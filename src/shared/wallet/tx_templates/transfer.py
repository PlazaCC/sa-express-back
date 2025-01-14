from decimal import Decimal
from src.shared.domain.enums.tx_status_enum import TX_STATUS

from src.shared.domain.entities.tx import TX

from src.shared.wallet.instructions.transfer import TXTransferInstruction

from src.shared.wallet.tx_templates.common import now_timestamp, \
    parse_build_params_user, parse_build_params_vault

def create_transfer_tx(build_params: dict) -> TX:
    user_id = parse_build_params_user(build_params)

    from_vault = parse_build_params_vault(build_params, 'from', True)
    to_vault = parse_build_params_vault(build_params, 'to', True)

    amount = Decimal(build_params['amount'])

    transfer_instr = TXTransferInstruction(from_vault, to_vault, amount)

    return TX(
        tx_id=TX.random_id(),
        user_id=user_id,
        create_timestamp=now_timestamp(),
        sign_timestamp=None,
        commit_timestamp=None,
        vaults=[ from_vault, to_vault ],
        instructions=[ transfer_instr ],
        logs=[],
        status=TX_STATUS.NEW
    )