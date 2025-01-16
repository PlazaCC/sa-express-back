import asyncio

from src.shared.domain.entities.tx import TX
from src.shared.domain.entities.user import User
from src.shared.domain.enums.tx_status_enum import TX_STATUS
from src.shared.domain.enums.vault_type_num import VAULT_TYPE

from src.shared.wallet.utils import now_timestamp, error_with_instruction_sufix
from src.shared.wallet.vault_processor import VaultProcessor
from src.shared.wallet.tx_instruction_results.base import TXBaseInstructionResult
from src.shared.wallet.tx_results.sign import TXSignResult

class TXProcessor:
    MAX_VAULTS=2
    MAX_INSTRUCTIONS=1

    def __init__(self, cache, repository, paygate):
        self.cache = cache
        self.repository = repository

        self.paygate = paygate
        self.vault_proc = VaultProcessor(cache, repository)

    async def sign(self, signer: User, tx: TX) -> TXSignResult:
        fields_error = self.validate_tx_fields_before_sign(tx)
        
        if fields_error is not None:
            return TXSignResult.failed(fields_error)
        
        tx.user_id = signer.user_id
        tx.logs = {}
        
        signer_access_error = self.validate_signer_access(signer, tx)

        if signer_access_error is not None:
            return TXSignResult.failed(signer_access_error)

        await self.vault_proc.lock(tx.vaults)

        sim_state, sim_results = await self.exec_tx_instructions(tx, from_sign=True)

        if sim_state['error'] is not None:
            return TXSignResult.failed(sim_state['error'])

        if not sim_state['any_promise']:
            return await self.commit_from_sign(tx, sim_state)
        
        # TODO: handle request errors
        logs = await asyncio.gather(*[ txr.call_promise(self) for txr in sim_results if txr.with_promise() ])

        tx_logs = {}

        for log in logs:
            if log.with_error():
                return TXSignResult.failed(log.error)

            tx_logs[log.key] = log
        
        tx.logs = tx_logs
        tx.status = TX_STATUS.SIGNED
        tx.sign_timestamp = now_timestamp()

        for vault in tx.vaults:
            if vault.type == VAULT_TYPE.SERVER_UNLIMITED:
                continue

            vault_key = vault.to_identity_key()
            vault_state = sim_state['vaults'][vault_key]

            vault.balanceLocked = vault_state['balanceLocked']

            # TODO: handle cache/rep errors
            await self.vault_proc.persist_vault(vault)

        # TODO: handle repository errors
        await self.repository.set_transaction(tx)
        
        await self.vault_proc.unlock(tx.vaults)
        
        return None
    
    def validate_tx_fields_before_sign(self, tx: TX) -> str | None:
        if tx.status != TX_STATUS.NEW:
            return 'Unsignable transaction status'

        if tx.sign_timestamp is not None:
            return 'Transaction already signed'
        
        if tx.commit_timestamp is not None:
            return 'Transaction already commited'
        
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
    
    async def exec_tx_instructions(self, tx: TX, from_sign: bool) -> tuple[dict, list[TXBaseInstructionResult | None]]:
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

        num_instructions = len(tx.instructions)

        results = [ None for _ in range(0, num_instructions) ]

        for i in range(0, num_instructions):
            next_state, instr_result = await tx.instructions[i].execute(i, state, from_sign)

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

            vault.locked = False
            vault.update_state(vault_state)

            # TODO: handle cache/rep errors
            await self.vault_proc.persist_vault(vault)

        tx.status = TX_STATUS.COMMITED

        now = now_timestamp()

        tx.sign_timestamp = now
        tx.commit_timestamp = now

        # TODO: handle repository errors
        await self.repository.set_transaction(tx)

        return TXSignResult.successful()