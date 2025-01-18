from src.shared.domain.enums.tx_status_enum import TX_STATUS
from src.shared.domain.entities.tx import TX

from src.shared.wallet.decimal import Decimal
from src.shared.wallet.utils import now_timestamp
from src.shared.wallet.tx_instructions.transfer import TXTransferInstruction
from src.shared.wallet.tx_templates.common import parse_build_params_user, \
    parse_build_params_vault

def create_withdrawal_tx(build_params: dict) -> TX:
    user_id = parse_build_params_user(build_params)

    from_vault = parse_build_params_vault(build_params, 'from', False)
    to_vault = parse_build_params_vault({ 'server': True }, '', True)

    amount = Decimal(build_params['amount'])

    transfer_instr = TXTransferInstruction(from_vault, to_vault, amount)

    return TX(
        tx_id=TX.random_id(),
        user_id=-1 if user_id is None else user_id,
        create_timestamp=now_timestamp(),
        vaults=[ from_vault, to_vault ],
        instructions=[ transfer_instr ],
        logs={},
        status=TX_STATUS.NEW,
        sign_result=None,
        commit_result=None
    )