import uuid
import pytest
import random
import asyncio
from decimal import Decimal
from datetime import datetime

from src.shared.domain.entities.user import User
from src.shared.domain.entities.vault import Vault
from src.shared.domain.entities.tx import TX

from src.shared.wallet.tx_processor import TXProcessor
from src.shared.wallet.instructions.transfer import TXTransferInstruction

from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.user_status_enum import USER_STATUS
from src.shared.domain.enums.tx_status_enum import TX_STATUS

pytest_plugins = ('pytest_asyncio')

class CacheMock:
    def __init__(self):
        self.vaults_by_user_id = {}

    async def get_vault_by_user_id(self, user_id: int):
        if user_id in self.vaults_by_user_id:
            return None, Vault.from_dict_static(self.vaults_by_user_id[user_id])

        return None, None
    
    async def set_vault(self, vault):
        self.vaults_by_user_id[vault.user_id] = vault.to_dict()

        return None, vault.user_id

class RepositoryMock:
    def __init__(self):
        self.users = []
        self.vaults = []

    def _generate_users(self, config):
        num = config['num'] if 'num' in config else 1

        roleList = config['role'] if 'role' in config else ([ r.value for r in ROLE ])
        userStatusList = config['userStatus'] if 'userStatus' in config else ([ s.value for s in USER_STATUS ])

        now = datetime.now()

        users = []

        for i in range(num):
            name = 'user-mock-' + str(i)

            role = random.choice(roleList)
            userStatus = random.choice(userStatusList)

            user = User.from_dict_static({
                "user_id": i,
                "name": name,
                "email": i,
                "role": role,
                "user_status": userStatus,
                "created_at": str(now.timestamp()),
                "updated_at": str(now.timestamp()),
                "email_verified": True,
                "enabled": True
            })

            users.append(user.to_dict())

        return users

    def generate_users(self, config):
        users = self._generate_users(config)

        if 'append' in config:
            self.users += users
        else:
            self.users = users

        return self.users

    async def get_vault_by_user_id(self, user_id):
        rep_vault = next((v for v in self.vaults if v['user_id'] == user_id), None)

        return (None, Vault.from_dict_static(rep_vault)) if rep_vault is not None else (None, None)
    
    async def set_vault(self, vault):
        (get_error, rep_vault) = await self.get_vault_by_user_id(vault.user_id)

        if get_error is not None:
            return get_error, None

        if rep_vault is not None:
            return None, rep_vault.user_id

        self.vaults.append(vault.to_dict())

        return None, vault.user_id

    def get_all_users(self):
        return ([ User.from_dict_static(u) for u in self.users ])

    def get_random_user(self):
        return User.from_dict_static(random.choice(self.users))
    
    def get_random_vault(self):
        user = self.get_random_user()

        rep_vault = next((v for v in self.vaults if v['user_id'] == user.user_id), None)

        return Vault.from_dict_static(rep_vault) if rep_vault is not None else None

class PayGateMock:
    def __init__(self):
        pass

    async def create_pix(self):
        pass

class Test_TXMock:
    def get_back_context(self):
        cache = CacheMock()
        repository = RepositoryMock()
        pay_gate = PayGateMock()

        repository.generate_users({
            'num': 10,
            'userStatus': [ USER_STATUS.CONFIRMED.value ]
        })

        return (cache, repository, pay_gate)

    @pytest.mark.asyncio
    async def test_vaults(self):
        (cache, repository, pay_gate) = self.get_back_context()
        
        tx_proc = TXProcessor(cache, repository, pay_gate)

        users = repository.get_all_users()

        total_balance = 0

        for user in users:
            config = { 'balance': str(random.uniform(1000, 10000)), 'locked': True }

            (vault_error, user_vault) = await tx_proc.vault_proc.create_if_not_exists(user, config)

            assert vault_error is None

            total_balance += user_vault.balance

        assert len([ k for k in cache.vaults_by_user_id ]) > 0
        assert total_balance > 0
    
    @pytest.mark.asyncio
    async def test_deposits(self):
        (cache, repository, pay_gate) = self.get_back_context()

        tx_proc = TXProcessor(cache, repository, pay_gate)

        # create tx
        # validate tx
        # call paygate and wait webhook
        # execute instructions and update vaults
        # verify if zero sum

        assert True

    @pytest.mark.asyncio
    async def test_withdrawals(self):
        assert True