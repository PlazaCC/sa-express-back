from src.environments import STAGE, Environments
from src.shared.domain.repositories.deal_repository_interface import IDealRepository
from src.shared.infra.repositories.database.deal_repository_dynamo import DealRepositoryDynamo
from src.shared.infra.repositories.mocks.deal_repository_mock import DealRepositoryMock


class Repository:
    deal_repo: IDealRepository

    def __init__(
            self,
            deal_repo: bool = False,
    ):
        self.session = None

        if Environments.stage == STAGE.TEST:
            self._initialize_mock_repositories(
                 deal_repo
            )
        else:
            self._initialize_database_repositories(
                deal_repo
            )

    def _initialize_mock_repositories(self, deal_repo):
        if deal_repo:
            self.deal_repo = DealRepositoryMock()
        
    def _initialize_database_repositories(self, deal_repo):
        if deal_repo:
            self.deal_repo = DealRepositoryDynamo()