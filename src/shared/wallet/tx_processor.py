import asyncio
from urllib import parse

from src.shared.domain.entities.tx import TX
from src.shared.domain.entities.user import User
from src.shared.domain.enums.tx_status_enum import TX_STATUS
from src.shared.domain.enums.vault_type_num import VAULT_TYPE

from src.shared.wallet.utils import error_with_instruction_sufix
from src.shared.wallet.enums.paygate_tx_status import PAYGATE_TX_STATUS
from src.shared.wallet.vault_processor import VaultProcessor
from src.shared.wallet.tx_logs import TXLogs
from src.shared.wallet.tx_instruction_results.base import TXBaseInstructionResult
from src.shared.wallet.tx_results.sign import TXSignResult
from src.shared.wallet.tx_results.commit import TXCommitResult

class TXProcessor:
    MAX_VAULTS=2
    MAX_INSTRUCTIONS=1

    def __init__(self, cache, repository, paygate):
        self.cache = cache
        self.repository = repository

        self.paygate = paygate
        self.vault_proc = VaultProcessor(cache, repository)

    async def persist_tx(self, tx: TX) -> None:
        await asyncio.gather(self.cache.set_transaction(tx), self.repository.set_transaction(tx))

        return None
    
    def get_tx_committed_stage(self, tx: TX) -> TX_STATUS:
        all_resolved = True

        for _, log in tx.logs.items():
            if not log.resolved:
                all_resolved = False
                break
        
        return TX_STATUS.COMMITTED if all_resolved else TX_STATUS.PARTIALLY_COMMITTED
        
    async def sign(self, signer: User, tx: TX) -> TXSignResult:
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

        # TODO: handle real cache errors
        tx.vaults = await self.vault_proc.lock(tx.vaults)

        sim_state, sim_results = await self.exec_tx_instructions(tx, from_sign=True)

        if sim_state['error'] is not None:
            tx.sign_result = TXSignResult.failed(sim_state['error'])

            return tx.sign_result

        if not sim_state['any_promise']:
            return await self.commit_from_sign(tx, sim_state)
        
        # TODO: handle real request errors
        logs = await asyncio.gather(*[ txr.call_promise(self) for txr in sim_results if txr.with_promise() ])

        tx_logs = {}

        for log in logs:
            if log.with_error():
                return TXSignResult.failed(log.error)

            tx_logs[log.key] = log

        tx.logs = tx_logs
        tx.status = TX_STATUS.SIGNED
        tx.sign_result = TXSignResult.successful()

        for vault in tx.vaults:
            if vault.type == VAULT_TYPE.SERVER_UNLIMITED:
                continue

            vault_key = vault.to_identity_key()
            vault_state = sim_state['vaults'][vault_key]

            vault.balance_locked = vault_state['balance_locked']

            # TODO: handle real cache/rep errors
            await self.vault_proc.persist_vault(vault)

        # TODO: handle real cache/rep errors
        await self.persist_tx(tx)
        
        # TODO: handle real cache errors
        await self.vault_proc.unlock(tx.vaults)

        sign_result = tx.sign_result.clone()

        for log in logs:
            if log.populate_sign_data is not None:
                for (field_key, field_value) in log.populate_sign_data():
                    sign_result.data[field_key] = field_value
        
        return sign_result
    
    def validate_tx_fields_before_sign(self, tx: TX) -> str | None:
        if tx.status != TX_STATUS.NEW:
            return 'Unsignable transaction status'

        if tx.sign_result is not None or tx.commit_result is not None:
            return 'Transaction already signed'
        
        num_vaults = len(tx.vaults)

        if num_vaults == 0:
            return 'Transaction without vaults'
        
        if num_vaults > TXProcessor.MAX_VAULTS:
            return f'Transaction with too many vaults (MAX {TXProcessor.MAX_VAULTS})'

        num_instructions = len(tx.instructions)

        if num_instructions == 0:
            return 'Transaction without instructions'

        if num_instructions > TXProcessor.MAX_INSTRUCTIONS:
            return f'Transaction with too many instructions (MAX {TXProcessor.MAX_INSTRUCTIONS})'
        
        for i in range(0, num_instructions):
            instr_fields_error = tx.instructions[i].validate_fields_before_sign()

            if instr_fields_error is not None:
                return instr_fields_error + f' at instruction {str(i)}'

        vault_match_error = self.bidirectional_vault_matching(tx)

        if vault_match_error is not None:
            return vault_match_error

        return None
    
    def bidirectional_vault_matching(self, tx: TX) -> str | None:
        forward_vaults = {}

        for vault in tx.vaults:
            vault_key = vault.to_identity_key()

            if vault_key not in forward_vaults:
                forward_vaults[vault_key] = True
                continue

            return f'Duplicated vault "{vault_key}"'

        backward_vaults = {}

        for instruction in tx.instructions:
            for vault in instruction.get_vaults():
                vault_key = vault.to_identity_key()

                if vault_key in forward_vaults:
                    del forward_vaults[vault_key]

                if vault_key not in backward_vaults:
                    backward_vaults[vault_key] = True

        if len(forward_vaults) != 0:
            return 'Transaction vault forward matching failed'

        for vault in tx.vaults:
            vault_key = vault.to_identity_key()

            if vault_key in backward_vaults:
                del backward_vaults[vault_key]

        if len(backward_vaults) != 0:
            return 'Transaction vault backward matching failed'

        return None
    
    def validate_signer_access(self, signer: User, tx: TX) -> str | None:
        for i in range(0, len(tx.instructions)):
            signer_access_error = tx.instructions[i].validate_signer_access(signer)

            if signer_access_error is not None:
                return error_with_instruction_sufix(signer_access_error, i)

        return None
    
    def get_tx_state(self, tx: TX) -> dict:
        state = {
            'tx_id': tx.tx_id,
            'error': None,
            'vaults': {},
            'any_promise': False 
        }
        
        for vault in tx.vaults:
            vault_key, vault_state = vault.to_tx_execution_state()

            if vault_key not in state['vaults']:
                state['vaults'][vault_key] = vault_state

        return state

    async def exec_tx_instructions(self, tx: TX, from_sign: bool) -> tuple[dict, list[TXBaseInstructionResult | None]]:
        state = self.get_tx_state(tx)

        num_instructions = len(tx.instructions)

        results = [ None for _ in range(0, num_instructions) ]

        for i in range(0, num_instructions):
            instruction = tx.instructions[i]

            instruction.update_vaults(tx.vaults)

            next_state, instr_result = await instruction.execute(i, state, from_sign)

            results[i] = instr_result

            if instr_result.with_error():
               state['error'] = error_with_instruction_sufix(instr_result.error, i)
               break
            
            if instr_result.promise is not None:
                state['any_promise'] = True
            
            state = next_state

        return state, results

    async def commit_from_sign(self, tx: TX, exec_state: dict) -> TXSignResult:
        for vault in tx.vaults:
            if vault.type == VAULT_TYPE.SERVER_UNLIMITED:
                continue

            vault_key = vault.to_identity_key()
            vault_state = exec_state['vaults'][vault_key]

            # TODO: handle real cache errors
            vault.update_state(vault_state)

            # TODO: handle real cache/rep errors
            await self.vault_proc.persist_vault(vault)

        tx.status = TX_STATUS.COMMITED
        
        tx.sign_result = TXSignResult.successful()
        tx.commit_result = TXCommitResult.successful()

        # TODO: handle real cache/rep errors
        await self.persist_tx(tx)
        
        # TODO: handle real cache errors
        await self.vault_proc.unlock(tx.vaults)

        return tx.sign_result
    
    async def get_tx_by_paygate_ref(self, paygate_ref: str) -> tuple[TX, int] | tuple[None, None]:
        try:
            qs = dict(parse.parse_qsl(paygate_ref))
        except:
            return (None, None)
        
        if 'TX' not in qs or TX.invalid_tx_id(qs['TX']):
            return (None, None)
        
        if 'INSTR' not in qs:
            return (None, None)
        
        instr_index = int(qs['INSTR']) if qs['INSTR'].isdecimal() else None

        if instr_index is None or instr_index < 0:
            return (None, None)

        # TODO: verify cache first
        (_, rep_tx) = await self.repository.get_transaction(qs['TX'])

        if rep_tx is None:
            return (None, None)
        
        if instr_index >= len(rep_tx.instructions):
            return (None, None)

        return (rep_tx, instr_index)

    async def commit_tx(self, tx: TX, instr_index: int, paygate_tx_status: PAYGATE_TX_STATUS) -> TXCommitResult:
        if paygate_tx_status == PAYGATE_TX_STATUS.FAILED:
            return await self.commit_tx_failed(tx, instr_index)

        if paygate_tx_status == PAYGATE_TX_STATUS.CONFIRMED:
            return await self.commit_tx_confirmed(tx, instr_index)

    async def commit_tx_failed(self, tx: TX, instr_index: int) -> TXCommitResult:
        return TXCommitResult.successful()

    async def commit_tx_confirmed(self, tx: TX, instr_index: int) -> TXCommitResult:
        log_key = TXLogs.get_instruction_log_key(instr_index)

        if log_key not in tx.logs:
            return TXCommitResult.failed(f'Transaction log not found: "{log_key}"')

        commit_log = tx.logs[log_key]

        if commit_log.resolved:
            return TXCommitResult.failed(f'Transaction log already resolved: "{log_key}"')

        instruction = tx.instructions[instr_index]

        # TODO: handle real cache errors
        tx.vaults = await self.vault_proc.lock(tx.vaults)

        state = self.get_tx_state(tx)

        instruction.update_vaults(tx.vaults)

        next_state, instr_result = await instruction.execute(instr_index, state, from_sign=False)

        if instr_result.with_error():
            error = error_with_instruction_sufix(instr_result.error, instr_index)

            commit_log.resolved = True
            commit_log.error = instr_result.error

            tx.status = self.get_tx_committed_stage(tx)
            tx.commit_result = TXCommitResult.failed(error)
            
            # TODO: handle real cache/rep errors
            await self.persist_tx(tx)

            # TODO: handle real cache errors
            await self.vault_proc.unlock(tx.vaults)

            return tx.commit_result

        for vault in instruction.get_vaults():
            if vault.type == VAULT_TYPE.SERVER_UNLIMITED:
                continue

            vault_key = vault.to_identity_key()
            vault_state = next_state['vaults'][vault_key]

            # TODO: handle real rep errors
            vault.update_state(vault_state)

            # TODO: handle real cache/rep errors
            await self.vault_proc.persist_vault(vault)
        
        commit_log.resolved = True
        commit_log.error = ''
        
        tx.status = self.get_tx_committed_stage(tx)
        tx.commit_result = TXCommitResult.successful()

        # TODO: handle real cache/rep errors
        await self.persist_tx(tx)
        
        # TODO: handle real cache errors
        await self.vault_proc.unlock(tx.vaults)

        return tx.commit_result

