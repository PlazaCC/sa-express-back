from src.shared.environments import STAGE, Environments
from src.shared.domain.repositories.deal_repository_interface import IDealRepository
from src.shared.infra.external.dynamo_datasource import DynamoDatasource
from src.shared.infra.repositories.auth.auth_repository_cognito import AuthRepositoryCognito
from src.shared.infra.repositories.database.deal_repository_dynamo import DealRepositoryDynamo
from src.shared.infra.repositories.mocks.deal_repository_mock import DealRepositoryMock


class Repository:
    deal_repo: IDealRepository

    def __init__(
            self,
            deal_repo: bool = False,
            auth_repo: bool = False
    ):
        if Environments.stage == STAGE.TEST:
            self._initialize_mock_repositories(
                 deal_repo
            )
        else:
            self._initialize_database_repositories(
                deal_repo,
                auth_repo
            )

    def _initialize_mock_repositories(self, deal_repo):
        if deal_repo:
            self.deal_repo = DealRepositoryMock()
        
    def _initialize_database_repositories(self, deal_repo, auth_repo):
        dynamo = DynamoDatasource(
            dynamo_table_name=Environments.get_envs().dynamo_table_name,
            region=Environments.get_envs().region,
        )
        if deal_repo:
            self.deal_repo = DealRepositoryDynamo(dynamo)
        if auth_repo:
            self.auth_repo = AuthRepositoryCognito()