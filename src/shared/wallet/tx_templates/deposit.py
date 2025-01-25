from src.shared.domain.enums.tx_status_enum import TX_STATUS
from src.shared.domain.entities.tx import TX

from src.shared.wallet.decimal import Decimal
from src.shared.wallet.utils import now_timestamp
from src.shared.wallet.tx_instructions.transfer import TXTransferInstruction
from src.shared.wallet.tx_templates.common import parse_build_params_user, \
    parse_build_params_vault

def create_deposit_tx(build_params: dict) -> TX:
    user_id = parse_build_params_user(build_params)

    from_vault = parse_build_params_vault({ 'server': True }, '', True)
    to_vault = parse_build_params_vault(build_params, 'to', False)

    amount = Decimal(build_params['amount'])

    transfer_instr = TXTransferInstruction(from_vault, to_vault, amount)

    return TX(
        tx_id=TX.random_id(),
        user_id=-1 if user_id is None else user_id,
        create_timestamp=now_timestamp(),
        instruction=transfer_instr,
        logs=None,
        status=TX_STATUS.NEW,
        sign_result=None,
        commit_result=None,
        description=build_params['description'] if 'description' in build_params else ''
    )