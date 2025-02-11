import pytest

from tests.shared.wallet.aws_lambda.common import load_app_env

load_app_env()

from src.shared.infra.repositories.repository import Repository

class Test_Repo:
    ### TEST METHODS ###
    # @pytest.mark.skip(reason='')
    def test_basic(self):
        repository = Repository(wallet_repo=True, wallet_cache=True)

        print(repository)
        
        assert True