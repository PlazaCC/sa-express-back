import pytest

from tests.shared.wallet.aws_lambda.common import load_app_env

load_app_env()

from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

from src.shared.wallet.vault_processor import VaultProcessor
from src.shared.wallet.mocks.wallet_paygate_mock import WalletPayGateMock

class Test_Repo:
    ### TEST METHODS ###
    # @pytest.mark.skip(reason='')
    def test_create_vault(self):
        base_repository = Repository(wallet_repo=True, wallet_cache=True)

        cache = base_repository.wallet_cache
        repository = base_repository.wallet_repo

        user = AuthAuthorizerDTO.from_api_gateway({
            'user_id': 0,
            'name': 'testuser',
            'email': 'testuser@gmail.com',
            'role': 'SUBAFILIADO',
            'email_verified': True
        })

        vault_proc = VaultProcessor(cache, repository)

        vault_proc.create_if_not_exists(user)

        cache_vault = cache.get_vault_by_user_id(user.user_id)

        assert cache_vault is not None
        
        rep_vault = repository.get_vault_by_user_id(user.user_id)

        assert rep_vault is not None

    # @pytest.mark.skip(reason='')
    def test_lock_script(self):
        assert True