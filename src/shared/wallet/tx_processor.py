import asyncio
from urllib import parse
from typing import Awaitable
from collections.abc import Callable

from src.shared.domain.enums.tx_status_enum import TX_STATUS
from src.shared.domain.enums.vault_type_num import VAULT_TYPE
from src.shared.domain.entities.tx import TX
from src.shared.domain.entities.user import User
from src.shared.infra.repositories.dtos.user_api_gateway_dto import UserApiGatewayDTO
from src.shared.domain.repositories.wallet_cache_interface import IWalletCache
from src.shared.domain.repositories.wallet_repository_interface import IWalletRepository

from src.shared.wallet.enums.tx_queue_type import TX_QUEUE_TYPE
from src.shared.wallet.vault_processor import VaultProcessor
from src.shared.wallet.tx_logs import TXLogs
from src.shared.wallet.tx_instruction_results.base import TXBaseInstructionResult
from src.shared.wallet.tx_results.sign import TXSignResult
from src.shared.wallet.tx_results.commit import TXCommitResult
from src.shared.wallet.tx_results.push import TXPushResult
from src.shared.wallet.tx_results.pop import TXPopResult
from src.shared.wallet.tx_queues.base import TXBaseQueue
from src.shared.wallet.tx_queues.client import TXClientQueue
from src.shared.wallet.tx_queues.server_single import TXServerSingleQueue
from src.shared.wallet.tx_queues.single_multi import TXServerMultiQueue
from src.shared.wallet.wrappers.paygate import IWalletPayGate

class TXProcessorConfig:
    tx_queue_type: TX_QUEUE_TYPE

    @staticmethod
    def default() -> 'TXProcessorConfig':
        return TXProcessorConfig()
    
    def __init__(self, tx_queue_type: TX_QUEUE_TYPE = TX_QUEUE_TYPE.CLIENT):
        self.tx_queue_type = tx_queue_type

    def to_dict(self):
        return {
            'tx_queue_type': self.tx_queue_type.value
        }

class TXProcessor:
    cache: IWalletCache
    repository: IWalletRepository
    paygate: IWalletPayGate
    config: TXProcessorConfig
    tx_queue: TXBaseQueue
    vault_proc: VaultProcessor

    def __init__(self, cache: IWalletCache, repository: IWalletRepository, paygate: IWalletPayGate, \
        config: TXProcessorConfig = TXProcessorConfig.default()):
        self.cache = cache
        self.repository = repository
        self.paygate = paygate
        self.config = config
        
        if self.config.tx_queue_type == TX_QUEUE_TYPE.CLIENT:
            self.tx_queue = TXClientQueue(self)
        elif self.config.tx_queue_type == TX_QUEUE_TYPE.SERVER_SINGLE:
            self.tx_queue = TXServerSingleQueue(self)
        elif self.config.tx_queue_type == TX_QUEUE_TYPE.SERVER_MULTI:
            self.tx_queue = TXServerMultiQueue(self)
        
        self.vault_proc = VaultProcessor(cache, repository)
    
    ### UTILITY METHODS ###
    def persist_tx(self, tx: TX) -> None:
        self.cache.upsert_transaction(tx)
        self.repository.upsert_transaction(tx)
        
        return None

    async def exec_tx_instruction(self, tx: TX, from_sign: bool) -> tuple[dict, TXBaseInstructionResult | None]:
        state = self.get_tx_state(tx)

        instruction = tx.instruction

        next_state, instr_result = await instruction.execute(state, from_sign)

        if instr_result.with_error():
            state['error'] = instr_result.error
            
            return state, None
        
        if instr_result.promise is not None:
            state['with_promise'] = True
        
        state = next_state

        return state, instr_result

    def validate_tx_fields_before_sign(self, tx: TX) -> str | None:
        if tx.status != TX_STATUS.NEW:
            return 'Unsignable transaction status'

        if tx.sign_result is not None or tx.commit_result is not None:
            return 'Transaction already signed'

        instr_fields_error = tx.instruction.validate_fields_before_sign()

        if instr_fields_error is not None:
            return instr_fields_error

        return None
    
    def validate_signer_access(self, signer: User | UserApiGatewayDTO, tx: TX) -> str | None:
        signer_access_error = tx.instruction.validate_signer_access(signer)

        if signer_access_error is not None:
            return signer_access_error

        return None
    
    def get_tx_state(self, tx: TX) -> dict:
        state = {
            'tx_id': tx.tx_id,
            'error': None,
            'vaults': {},
            'with_promise': False 
        }
        
        for vault in tx.instruction.get_vaults():
            vault_key, vault_state = vault.to_tx_execution_state()

            if vault_key not in state['vaults']:
                state['vaults'][vault_key] = vault_state

        return state

    def get_tx_by_paygate_ref(self, paygate_ref: str) -> TX | None:
        try:
            qs = dict(parse.parse_qsl(paygate_ref))
        except:
            return (None, None)
        
        if 'TX' not in qs or TX.invalid_tx_id(qs['TX']):
            return (None, None)
    
        rep_tx = self.repository.get_transaction(qs['TX'])

        if rep_tx is None:
            return (None, None)

        return rep_tx
    
    ### SIGN METHODS ###
    async def sign(self, signer: User | UserApiGatewayDTO, tx: TX) -> TXSignResult:
        fields_error = self.validate_tx_fields_before_sign(tx)
        
        if fields_error is not None:
            tx.sign_result = TXSignResult.failed(fields_error)

            return tx.sign_result
        
        tx.user_id = signer.user_id
        tx.logs = {}
        
        signer_access_error = self.validate_signer_access(signer, tx)

        if signer_access_error is not None:
            tx.sign_result = TXSignResult.failed(signer_access_error)

            return tx.sign_result

        sim_state, sim_result = await self.exec_tx_instruction(tx, from_sign=True)

        if sim_state['error'] is not None:
            tx.sign_result = TXSignResult.failed(sim_state['error'])

            return tx.sign_result

        if not sim_state['with_promise']:
            return await self.commit_from_sign(tx, sim_state)
        
        logs = await sim_result.call_promise(self)

        if logs.with_error():
            return TXSignResult.failed(logs.error)

        tx.logs = logs
        tx.status = TX_STATUS.SIGNED
        tx.sign_result = TXSignResult.successful()

        for vault in tx.instruction.get_vaults():
            if vault.type == VAULT_TYPE.SERVER_UNLIMITED:
                continue

            vault_key = vault.to_identity_key()
            vault_state = sim_state['vaults'][vault_key]

            vault.balance_locked = vault_state['balance_locked']

            self.vault_proc.persist_vault(vault)
        
        self.persist_tx(tx)

        sign_result = tx.sign_result.clone()

        if logs.populate_sign_data is not None:
            for (field_key, field_value) in logs.populate_sign_data():
                sign_result.data[field_key] = field_value
        
        return sign_result

    async def commit_from_sign(self, tx: TX, exec_state: dict) -> TXSignResult:
        for vault in tx.instruction.get_vaults():
            if vault.type == VAULT_TYPE.SERVER_UNLIMITED:
                continue

            vault_key = vault.to_identity_key()
            vault_state = exec_state['vaults'][vault_key]

            vault.update_state(vault_state)

            self.vault_proc.persist_vault(vault)

        tx.status = TX_STATUS.COMMITED
        
        tx.sign_result = TXSignResult.successful()
        tx.commit_result = TXCommitResult.successful()

        self.persist_tx(tx)

        return tx.sign_result
    
    ### COMMIT METHODS ###
    async def commit_tx_failed(self, tx: TX, error: str = 'Unknown reason') -> TXCommitResult:
        if tx.status != TX_STATUS.SIGNED:
            return TXCommitResult.failed(f'Can\'t commit transaction with status "{tx.status.value}"')

        if tx.logs is None:
            return TXCommitResult.failed('Transaction logs is null')

        if tx.logs.resolved:
            return TXCommitResult.failed(f'Transaction logs already resolved')

        state = self.get_tx_state(tx)

        next_state, instr_result = await tx.instruction.revert(state)

        if instr_result.with_error():
            return await self.commit_failed_epilogue(tx, instr_result)
        
        for vault in tx.instruction.get_vaults():
            if vault.type == VAULT_TYPE.SERVER_UNLIMITED:
                continue

            vault_key = vault.to_identity_key()
            vault_state = next_state['vaults'][vault_key]

            vault.update_state(vault_state)

            self.vault_proc.persist_vault(vault)
        
        tx.logs.resolved = True
        tx.logs.error = ''
        
        tx.status = TX_STATUS.COMMITTED
        tx.commit_result = TXCommitResult.failed(error)

        self.persist_tx(tx)

        return tx.commit_result

    async def commit_tx_confirmed(self, tx: TX) -> TXCommitResult:
        if tx.status != TX_STATUS.SIGNED:
            return TXCommitResult.failed(f'Can\'t commit transaction with status "{tx.status.value}"')
        
        if tx.logs is None:
            return TXCommitResult.failed('Transaction logs is null')

        if tx.logs.resolved:
            return TXCommitResult.failed(f'Transaction log already resolved')

        state = self.get_tx_state(tx)

        next_state, instr_result = await tx.instruction.execute(state, from_sign=False)

        if instr_result.with_error():
            return await self.commit_failed_epilogue(tx, instr_result)

        for vault in tx.instruction.get_vaults():
            if vault.type == VAULT_TYPE.SERVER_UNLIMITED:
                continue

            vault_key = vault.to_identity_key()
            vault_state = next_state['vaults'][vault_key]

            vault.update_state(vault_state)

            self.vault_proc.persist_vault(vault)
        
        tx.logs.resolved = True
        tx.logs.error = ''
        
        tx.status = TX_STATUS.COMMITTED
        tx.commit_result = TXCommitResult.successful()

        self.persist_tx(tx)
        
        return tx.commit_result
    
    async def commit_failed_epilogue(self, tx: TX, instr_result: TXBaseInstructionResult) -> TXCommitResult:
        tx.logs.resolved = True
        tx.logs.error = instr_result.error

        tx.status = TX_STATUS.COMMITTED
        tx.commit_result = TXCommitResult.failed(instr_result.error)
        
        self.persist_tx(tx)

        return tx.commit_result
    
    ### QUEUE METHODS ###
    async def push_tx(self, signer: User | UserApiGatewayDTO, tx: TX) -> TXPushResult:
        return await self.tx_queue.push_tx(signer, tx)
    
    async def push_tx_with_callback(self, callback: Callable[[], Awaitable[TXPushResult]], signer: User | UserApiGatewayDTO, tx: TX) -> TXPushResult:
        return await self.tx_queue.push_tx(callback, signer, tx)
    
    async def pop_tx_with_callback(self, callback: Callable[[], Awaitable[TXPopResult]], tx: TX, error: str | None = None) -> TXPopResult:
        return await self.tx_queue.pop_tx(callback, tx, error)