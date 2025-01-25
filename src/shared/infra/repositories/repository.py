from src.shared.domain.repositories.affiliation_repository_interface import IAffiliationRepository
from src.shared.domain.repositories.entity_repository_interface import IEntityRepository
from src.shared.domain.repositories.profile_repository_interface import IProfileRepository
from src.shared.environments import STAGE, Environments
from src.shared.domain.repositories.deal_repository_interface import IDealRepository
from src.shared.infra.repositories.auth.auth_repository_cognito import AuthRepositoryCognito
from src.shared.infra.repositories.database.affiliation_repository_dynamo import AffiliationRepositoryDynamo
from src.shared.infra.repositories.database.deal_repository_dynamo import DealRepositoryDynamo
from src.shared.infra.repositories.database.entity_repository_dynamo import EntityRepositoryDynamo
from src.shared.infra.repositories.database.profile_repository_dynamo import ProfileRepositoryDynamo
from src.shared.infra.repositories.mocks.deal_repository_mock import DealRepositoryMock
from src.shared.infra.repositories.mocks.profile_repository_mock import ProfileRepositoryMock


class Repository:
    deal_repo: IDealRepository
    auth_repo: AuthRepositoryCognito
    profile_repo: IProfileRepository
    affiliation_repo: IAffiliationRepository
    entity_repo: IEntityRepository

    def __init__(
            self,
            deal_repo: bool = False,
            auth_repo: bool = False,
            profile_repo: bool = False,
            affiliation_repo: bool = False,
            entity_repo: bool = False
    ):
        if Environments.stage == STAGE.TEST:
            self._initialize_mock_repositories(
                 deal_repo,
                 profile_repo
            )
        else:
            self._initialize_database_repositories(
                deal_repo,
                auth_repo,
                profile_repo,
                affiliation_repo,
                entity_repo
            )
            

    def _initialize_mock_repositories(self, deal_repo, profile_repo):
        if deal_repo:
            self.deal_repo = DealRepositoryMock()
        if profile_repo:
            self.profile_repo = ProfileRepositoryMock()
        
    def _initialize_database_repositories(self, deal_repo, auth_repo, profile_repo, affiliation_repo, entity_repo):
        if deal_repo:
            self.deal_repo = DealRepositoryDynamo()
        if auth_repo:
            self.auth_repo = AuthRepositoryCognito()
        if profile_repo:
            self.profile_repo = ProfileRepositoryDynamo()
        if affiliation_repo:
            self.affiliation_repo = AffiliationRepositoryDynamo()
        if entity_repo:
            self.entity_repo = EntityRepositoryDynamo()