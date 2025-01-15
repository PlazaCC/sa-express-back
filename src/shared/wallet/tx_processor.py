import asyncio

from src.shared.domain.entities.tx import TX
from src.shared.domain.entities.user import User
from src.shared.domain.enums.tx_status_enum import TX_STATUS

from src.shared.wallet.vault_processor import VaultProcessor
from src.shared.wallet.tx_instruction_results.base import TXBaseInstructionResult

class TXProcessor:
    MAX_VAULTS=2
    MAX_INSTRUCTIONS=1

    def __init__(self, cache, repository, paygate):
        self.cache = cache
        self.repository = repository

        self.paygate = paygate
        self.vault_proc = VaultProcessor(cache, repository)

    async def sign(self, signer: User, tx: TX) -> str | None:
        fields_error = self.validate_tx_fields_before_sign(tx)
        
        if fields_error is not None:
            return fields_error
        
        tx.user_id = signer.user_id
        tx.logs = []
        
        signer_access_error = self.validate_signer_access(signer, tx)

        if signer_access_error is not None:
            return signer_access_error

        await self.vault_proc.lock(tx.vaults)

        sim_state, sim_results = await self.exec_tx_instructions(tx, from_sign=True)

        if sim_state['error'] is not None:
            return sim_state['error']

        if not sim_state['any_promise']:
            return await self.commit_with_state(tx, sim_state)
        
        txPromises = []

        for result in sim_results:
            for promise in result.promises:
                txPromises.append(promise)

        # TODO: handle request errors
        await asyncio.gather(*[ txp.call(self) for txp in txPromises ])

        tx.status = TX_STATUS.SIGNED

        # update balance locked (withdrawal)

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
                return signer_access_error + f' at instruction {str(i)}'

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

            if not instr_result.success:
               state['error'] = instr_result.error
               break

            if len(instr_result.promises) > 0:
                state['any_promise'] = True

            state = next_state

        return state, results

    async def commit_with_state(self, tx: TX, exec_state: dict) -> str | None:
        tx.status = TX_STATUS.COMMITED

        for vault in tx.vaults:
            vault_state = exec_state['vaults'][vault.to_identity_key()]

            vault.locked = False
            vault.update_state(vault_state)

            # TODO: handle cache/rep errors
            await asyncio.gather(self.cache.set_vault(vault), self.repository.set_vault(vault))

        # TODO: handle repository errors
        await self.repository.set_transaction(tx)

        return None