from src.environments import STAGE, Environments
from src.shared.domain.repositories.deal_repository_interface import IDealRepository
from src.shared.domain.repositories.wallet_repository_interface import IWalletRepository
from src.shared.domain.repositories.wallet_cache_interface import IWalletCache
from src.shared.infra.repositories.database.deal_repository_dynamo import DealRepositoryDynamo
from src.shared.infra.repositories.database.wallet_repository_dynamo import WalletRepositoryDynamo
from src.shared.infra.repositories.cache.wallet_cache_elastic import WalletCacheElastic
from src.shared.infra.repositories.mocks.deal_repository_mock import DealRepositoryMock
from src.shared.infra.repositories.mocks.wallet_repository_mock import WalletRepositoryMock
from src.shared.infra.repositories.mocks.wallet_cache_mock import WalletCacheMock

class Repository:
    deal_repo: IDealRepository
    wallet_repo: IWalletRepository
    wallet_cache: IWalletCache

    def __init__(
        self,
        deal_repo: bool = False,
        wallet_repo: bool = False,
        wallet_cache: bool = False
    ):
        self.session = None

        if Environments.stage == STAGE.TEST:
            self._initialize_mock_repositories(
                deal_repo,
                wallet_repo,
                wallet_cache
            )
        else:
            self._initialize_database_repositories(
                deal_repo,
                wallet_repo,
                wallet_cache
            )

    def _initialize_mock_repositories(self, deal_repo: bool, wallet_repo: bool, wallet_cache: bool) -> None:
        if deal_repo:
            self.deal_repo = DealRepositoryMock()

        if wallet_repo:
            self.wallet_repo = WalletRepositoryMock(singleton=True)

        if wallet_cache:
            self.wallet_cache = WalletCacheMock(singleton=True)
        
    def _initialize_database_repositories(self, deal_repo: bool, wallet_repo: bool, wallet_cache: bool) -> None:
        if deal_repo:
            self.deal_repo = DealRepositoryDynamo()

        if wallet_repo:
            self.wallet_repo = WalletRepositoryDynamo()

        if wallet_cache:
            self.wallet_cache = WalletCacheElastic()