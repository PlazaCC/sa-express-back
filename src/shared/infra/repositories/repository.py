from src.shared.domain.repositories.entity_repository_interface import IEntityRepository
from src.shared.environments import STAGE, Environments
from src.shared.infra.external.dynamo_datasource import DynamoDatasource
from src.shared.infra.repositories.auth.auth_repository_cognito import AuthRepositoryCognito
from src.shared.infra.repositories.database.entity_repository_dynamo import EntityRepositoryDynamo
from src.shared.infra.repositories.mocks.entity_repository_mock import EntityRepositoryMock


class Repository:
    entity_repo: IEntityRepository

    def __init__(
            self,
            entity_repo: bool = False,
            auth_repo: bool = False
    ):
        if Environments.stage == STAGE.TEST:
            self._initialize_mock_repositories(
                 entity_repo
            )
        else:
            self._initialize_database_repositories(
                entity_repo,
                auth_repo
            )

    def _initialize_mock_repositories(self, entity_repo):
        if entity_repo:
            self.entity_repo = EntityRepositoryMock()
        
    def _initialize_database_repositories(self, entity_repo, auth_repo):
        dynamo = DynamoDatasource(
            dynamo_table_name=Environments.dynamo_table_name,
            region=Environments.region,
        )
        if entity_repo:
            self.entity_repo = EntityRepositoryDynamo(dynamo)
        if auth_repo:
            self.auth_repo = AuthRepositoryCognito()