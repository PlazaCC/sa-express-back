from src.shared.domain.entities.vault import Vault

def parse_build_params_user(build_params: dict) -> int | None:
    user_id = None

    if 'user_id' in build_params:
        user_id = build_params['user_id']
    elif 'user' in build_params:
        user_id = build_params['user'].user_id

    return user_id

def parse_build_params_vault(build_params: dict, prefix: str, include_server=True) -> Vault | None:
    vault = None

    def concat_prefix(field_name: str):
        return prefix + '_' + field_name if len(prefix) > 0 else field_name
    
    vault_key = concat_prefix('vault')
    user_key = concat_prefix('user')
    user_id_key = concat_prefix('user_id')
    server_key = concat_prefix('server')

    if vault_key in build_params:
        vault = build_params[vault_key]
    elif user_key in build_params:
        vault = Vault.from_user(build_params[user_key])
    elif user_id_key in build_params:
        vault = Vault.from_user_id(build_params[user_id_key])
    elif include_server and server_key in build_params:
        vault = Vault.init_server_unlimited()

    return vault