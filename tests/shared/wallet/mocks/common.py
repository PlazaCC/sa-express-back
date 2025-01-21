import random

from src.shared.wallet.enums.pix import PIX_KEY_TYPE
from src.shared.wallet.models.pix import PIXKey
from src.shared.wallet.vault_processor import VaultProcessor
from src.shared.infra.repositories.mocks.wallet_cache_mock import WalletCacheMock
from src.shared.infra.repositories.mocks.wallet_repository_mock import WalletRepositoryMock

from src.shared.wallet.mocks.wallet_paygate_mock import WalletPayGateMock

async def get_back_context(config: dict):
    repository = WalletRepositoryMock()
    cache = WalletCacheMock()
    paygate = WalletPayGateMock()
    
    if 'num_users' in config and config['num_users'] > 0:
        repository.generate_users(config)

    if 'create_vaults' in config:
        create_vaults_config = config['create_vaults']
        
        vault_proc = VaultProcessor(cache, repository)

        users = repository.get_all_users()
        
        for user in users:
            vault_proc.create_if_not_exists(user, { 
                'balance': str(random.uniform(1000, 10000)) if create_vaults_config['random_balance'] else '0',
                'balance_locked': '0',
                'locked': create_vaults_config['locked']
            })

            pix_key = PIXKey(type=PIX_KEY_TYPE.CPF, value='00000000000')

            user_vault = repository.set_vault_pix_by_user_id(user.user_id, pix_key)
            
            cache.upsert_vault(user_vault)

    return (cache, repository, paygate)