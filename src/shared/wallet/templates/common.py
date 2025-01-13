from datetime import datetime
from src.shared.domain.entities.vault import Vault

def now_timestamp() -> str:
    return str(int(datetime.now().timestamp() * 1000))

def parse_build_params_user(build_params: dict) -> int | None:
    user_id = None

    if 'user_id' in build_params:
        user_id = build_params['user_id']
    elif 'user' in build_params:
        user_id = build_params['user'].user_id

    return user_id

def parse_build_params_vault(build_params: dict, prefix: str, include_server=True) -> Vault | None:
    vault = None

    vault_key = prefix + '_vault' if len(prefix) > 0 else 'vault'
    user_key = prefix + '_user' if len(prefix) > 0 else 'user'
    server_key = prefix + '_server' if len(prefix) > 0 else 'server'

    if vault_key in build_params:
        vault = build_params[vault_key]
    elif user_key in build_params:
        vault = Vault.from_user(build_params[user_key])
    elif 'from_user_id' in build_params:
        vault = Vault.from_user_id(build_params['from_user_id'])
    elif include_server and server_key in build_params:
        vault = Vault.init_server_unlimited()

    return vault