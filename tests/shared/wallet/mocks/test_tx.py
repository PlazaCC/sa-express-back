import pytest
import random
import asyncio
from decimal import Decimal
from random import randrange
from datetime import datetime

from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.vault_type_num import VAULT_TYPE
from src.shared.domain.enums.user_status_enum import USER_STATUS

from src.shared.domain.entities.user import User
from src.shared.domain.entities.vault import Vault
from src.shared.domain.entities.tx import TX

from src.shared.wallet.enums.pix import PIX_KEY_TYPE
from src.shared.wallet.enums.tx_queue_type import TX_QUEUE_TYPE
from src.shared.wallet.enums.paygate_tx_status import PAYGATE_TX_STATUS
from src.shared.wallet.models.pix import PIXKey
from src.shared.wallet.tx_processor import TXProcessor, TXProcessorConfig
from src.shared.wallet.vault_processor import VaultProcessor
from src.shared.wallet.tx_templates.deposit import create_deposit_tx
from src.shared.wallet.tx_templates.withdrawal import create_withdrawal_tx

pytest_plugins = ('pytest_asyncio')

class CacheMock:
    def __init__(self):
        self.vaults_by_user_id = {}
        self.vaults_by_server_ref = {}
        self.transactions = {}

    async def get_vault_by_user_id(self, user_id: int, deserialize: bool = True):
        if user_id in self.vaults_by_user_id:
            return None, Vault.from_dict_static(self.vaults_by_user_id[user_id]) if deserialize else self.vaults_by_user_id[user_id]

        return None, None
    
    async def get_vault_by_server_ref(self, server_ref: str, deserialize: bool = True):
        if server_ref in self.vaults_by_server_ref:
            return None, Vault.from_dict_static(self.vaults_by_server_ref[server_ref]) if deserialize else self.vaults_by_server_ref[server_ref]
        
        return None, None
    
    async def get_vault(self, vault: Vault, deserialize: bool = True):
        if vault.type == VAULT_TYPE.USER:
            return await self.get_vault_by_user_id(vault.user_id, deserialize)
        
        if vault.type == VAULT_TYPE.SERVER_LIMITED:
            return await self.get_vault_by_server_ref(vault.server_ref, deserialize)
    
    async def set_vault(self, vault: Vault) -> str | None:
        if vault.user_id is not None:
            self.vaults_by_user_id[vault.user_id] = vault.to_dict()

            return None
        
        if vault.server_ref is not None:
            self.vaults_by_server_ref[vault.server_ref] = vault.to_dict()

            return None

        return "Can't set vault without reference/id"
    
    async def set_transaction(self, tx: TX) -> str | None:
        self.transactions[tx.tx_id] = tx.to_tx_snapshot()

        return None
    
    def get_all_vaults(self) -> list[Vault]:
        user_vaults = [ Vault.from_dict_static(self.vaults_by_user_id[vk]) for vk in self.vaults_by_user_id ]
        server_vaults = [ Vault.from_dict_static(self.vaults_by_server_ref[vk]) for vk in self.vaults_by_server_ref ]

        return user_vaults + server_vaults
    
    async def lock_vault(self, vault: Vault) -> Vault:
        (_, updated_vault) = await self.get_vault(vault)

        updated_vault.locked = True

        await self.set_vault(updated_vault)

        return updated_vault
    
    async def unlock_vault(self, vault: Vault) -> Vault:
        (_, updated_vault) = await self.get_vault(vault)

        updated_vault.locked = False

        await self.set_vault(updated_vault)

        return updated_vault
    
    async def get_vaults_and_lock(self, vaults: list[Vault]) -> None | list[Vault]:
        cache_vaults = []

        async def _get_vault(v: Vault):
            if v.type == VAULT_TYPE.SERVER_UNLIMITED:
                return (None, v.to_dict())
            
            return await self.get_vault(v, deserialize=False)
        
        for (_, cache_vault) in await asyncio.gather(*[ _get_vault(v) for v in vaults ]):
            if cache_vault['locked']:
                return None
            
            cache_vaults.append(cache_vault)

        for cache_vault in cache_vaults:
            cache_vault['locked'] = True

        return [ Vault.from_dict_static(v) for v in cache_vaults ]

class RepositoryMock:
    def __init__(self):
        self.users = []
        self.vaults = []
        self.transactions = []

    def _generate_users(self, config: dict):
        num_users = config['num_users'] if 'num_users' in config else 1

        role_list = config['role'] if 'role' in config else ([ r.value for r in ROLE ])
        user_status_list = config['user_status'] if 'user_status' in config else ([ s.value for s in USER_STATUS ])

        now = datetime.now()

        users = []

        for i in range(num_users):
            name = 'user-mock-' + str(i)

            role = random.choice(role_list)
            user_status = random.choice(user_status_list)

            user = User.from_dict_static({
                "user_id": i,
                "name": name,
                "email": i,
                "role": role,
                "user_status": user_status,
                "created_at": str(now.timestamp()),
                "updated_at": str(now.timestamp()),
                "email_verified": True,
                "enabled": True
            })

            users.append(user.to_dict())

        return users

    def generate_users(self, config: dict):
        users = self._generate_users(config)

        if 'append' in config:
            self.users += users
        else:
            self.users = users

        return self.users

    async def get_user_by_user_id(self, user_id: int):
        rep_user = next((u for u in self.users if u['user_id'] == user_id), None)

        return (None, User.from_dict_static(rep_user)) if rep_user is not None else (None, None)

    async def get_vault_by_user_id(self, user_id: int):
        rep_vault = next((v for v in self.vaults if v['user_id'] == user_id), None)

        return (None, Vault.from_dict_static(rep_vault)) if rep_vault is not None else (None, None)
    
    async def set_vault(self, vault: Vault):
        (get_error, rep_vault) = await self.get_vault_by_user_id(vault.user_id)

        if get_error is not None:
            return get_error

        if rep_vault is not None:
            rep_vault_key = rep_vault.to_identity_key()

            self.vaults = [ v for v in self.vaults if Vault.from_dict_static(v).to_identity_key() != rep_vault_key ]

        self.vaults.append(vault.to_dict())

        return None

    def get_all_users(self):
        return ([ User.from_dict_static(u) for u in self.users ])

    def get_random_user(self):
        return User.from_dict_static(random.choice(self.users))
    
    def get_random_vault(self):
        user = self.get_random_user()

        rep_vault = next((v for v in self.vaults if v['user_id'] == user.user_id), None)

        return Vault.from_dict_static(rep_vault) if rep_vault is not None else None
    
    async def set_vault_pix_by_user_id(self, user_id: int, pix_key: PIXKey):
        (_, rep_vault) = await self.get_vault_by_user_id(user_id)

        if rep_vault is None:
            return None
        
        rep_vault.pix_key = pix_key

        return await self.set_vault(rep_vault)

    async def set_transaction(self, tx: TX):
        rep_tx = next((t for t in self.transactions if t['tx_id'] == tx.tx_id), None)
        
        if rep_tx is not None:
            self.transactions = [ t for t in self.transactions if t['tx_id'] != tx.tx_id ]

        self.transactions.append(tx.to_dict())

        return None
    
    async def get_transaction(self, tx_id: str):
        rep_tx = next((t for t in self.transactions if t['tx_id'] == tx_id), None)

        return (None, TX.from_dict_static(rep_tx)) if rep_tx is not None else (None, None)

class PayGateMock:
    def __init__(self):
        self.pending_payments = []

    async def create_pix_url(self, pix_key: PIXKey, paygate_ref: str) -> dict:
        self.pending_payments.append(paygate_ref)

        return {
            'data': {
                'pix_url': '00020126330014BR.GOV.BCB.PIX0111000000000005204000053039865406150.005802BR5904joao6009sao paulo621605121121212121216304E551'
            }
        }
    
    async def pix_withdraw(self, pix_key: PIXKey, paygate_ref: str) -> dict:
        self.pending_payments.append(paygate_ref)

        return {}

class Test_TXMock:
    async def get_back_context(self, config: dict):
        cache = CacheMock()
        repository = RepositoryMock()
        paygate = PayGateMock()

        if 'num_users' in config and config['num_users'] > 0:
            repository.generate_users(config)

        if 'create_vaults' in config:
            create_vaults_config = config['create_vaults']

            vault_proc = VaultProcessor(cache, repository)

            users = repository.get_all_users()

            for user in users:
                (vault_error, _) = await vault_proc.create_if_not_exists(user, { 
                    'balance': str(random.uniform(1000, 10000)) if create_vaults_config['random_balance'] else '0',
                    'balance_locked': '0',
                    'locked': create_vaults_config['locked']
                })

                assert vault_error is None

                pix_key = PIXKey(type=PIX_KEY_TYPE.CPF, value='00000000000')

                await repository.set_vault_pix_by_user_id(user.user_id, pix_key)

                (_, user_vault) = await repository.get_vault_by_user_id(user.user_id)
                
                await cache.set_vault(user_vault)

        return (cache, repository, paygate)

    @pytest.mark.asyncio
    @pytest.mark.skip(reason='')
    async def test_vaults(self):
        (cache, repository, paygate) = await self.get_back_context({
            'num_users': 10,
            'user_status': [ USER_STATUS.CONFIRMED.value ],
            'create_vaults': {
                'random_balance': True,
                'locked': False
            }
        })

        cached_vaults = cache.get_all_vaults()

        assert len(cached_vaults) > 0

        total_balance = 0

        for vault in cached_vaults:
            total_balance += vault.balance

        assert total_balance > 0
    
    @pytest.mark.asyncio
    @pytest.mark.skip(reason='')
    async def test_deposits(self):
        (cache, repository, paygate) = await self.get_back_context({
            'num_users': 10,
            'user_status': [ USER_STATUS.CONFIRMED.value ],
            'create_vaults': {
                'random_balance': False,
                'locked': False
            }
        })
        
        tx_proc = TXProcessor(cache, repository, paygate)
        
        txs = []

        for _ in range(0, 1):
            to_vault = repository.get_random_vault()
            (_, signer) = await repository.get_user_by_user_id(to_vault.user_id)

            amount = Decimal(150)
            
            tx = create_deposit_tx({ 'to_vault': to_vault, 'amount': amount })

            txs.append((signer, tx))

        assert(len(txs) > 0)

        await self.sign_txs(tx_proc, txs, [ PAYGATE_TX_STATUS.CONFIRMED ])

        assert True
    
    @pytest.mark.asyncio
    @pytest.mark.skip(reason='')
    async def test_withdrawals(self):
        (cache, repository, paygate) = await self.get_back_context({
            'num_users': 10,
            'user_status': [ USER_STATUS.CONFIRMED.value ],
            'create_vaults': {
                'random_balance': True,
                'locked': False
            }
        })
        
        tx_proc = TXProcessor(cache, repository, paygate)

        txs = []

        for _ in range(0, 1):
            from_vault = repository.get_random_vault()
            (_, signer) = await repository.get_user_by_user_id(from_vault.user_id)

            amount = from_vault.balance * Decimal(0.1)
            
            tx = create_withdrawal_tx({ 'from_vault': from_vault, 'amount': amount })

            txs.append((signer, tx))

        assert(len(txs) > 0)

        await self.sign_txs(tx_proc, txs, [ PAYGATE_TX_STATUS.CONFIRMED ])

        assert True
    
    async def sign_txs(self, tx_proc: TXProcessor, txs: list[TX], paygate_tx_status: list[PAYGATE_TX_STATUS]):
        webhooks = []

        async def random_paygate_webhook():
            await asyncio.sleep(randrange(1, 3))

            paygate_ref = tx_proc.paygate.pending_payments.pop()
            
            (tx, instr_index) = await tx_proc.get_tx_by_paygate_ref(paygate_ref)

            assert tx is not None
            assert instr_index is not None

            ptx_status = random.choice(paygate_tx_status)

            commit_result = await tx_proc.commit_tx(tx, instr_index, ptx_status)

            if ptx_status == PAYGATE_TX_STATUS.CONFIRMED:
                assert commit_result.without_error()
            elif ptx_status == PAYGATE_TX_STATUS.FAILED:
                assert commit_result.with_error()

        for (signer, tx) in txs:
            sign_result = await tx_proc.sign(signer, tx)
    
            assert sign_result.without_error()

            webhooks.append(random_paygate_webhook())

        await asyncio.gather(*webhooks)

    @pytest.mark.asyncio
    async def test_client_queue(self):
        (cache, repository, paygate) = await self.get_back_context({
            'num_users': 10,
            'user_status': [ USER_STATUS.CONFIRMED.value ],
            'create_vaults': {
                'random_balance': True,
                'locked': False
            }
        })

        tx_proc_config = TXProcessorConfig(
            max_vaults=2,
            max_instructions=1,
            tx_queue_type=TX_QUEUE_TYPE.CLIENT
        )

        tx_proc = TXProcessor(cache, repository, paygate, config=tx_proc_config)

        to_vault = repository.get_random_vault()
        (_, signer) = await repository.get_user_by_user_id(to_vault.user_id)

        amount = Decimal(150)
        
        tx = create_deposit_tx({ 'to_vault': to_vault, 'amount': amount })

        push_res = await tx_proc.push_tx(signer, tx)

        assert push_res.without_error()

        print('')
        print('push_res', push_res.to_dict())

        assert True