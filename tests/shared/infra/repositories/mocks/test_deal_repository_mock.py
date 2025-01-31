from src.shared.domain.entities.deal import Deal
from src.shared.domain.enums.deal_status_enum import DEAL_STATUS
from src.shared.infra.repositories.mocks.entity_repository_mock import DealRepositoryMock


class Test_DealRepositoryMock:

    def test_create_deal(self):
        repo = DealRepositoryMock()

        deal = Deal(deal_id="00000000-0000-0000-0000-000000000000", entity_id="00000000-0000-0000-0000-000000000000", baseline=1, cpa=1, rev_share=1, conditions="1", deal_status=DEAL_STATUS.ACTIVATED, created_at=1, updated_at=1)
        repo.create_deal(deal)

        assert repo.deals[0].deal_id == "00000000-0000-0000-0000-000000000000"
        assert len(repo.deals) == 3
    
    def test_get_deal_by_id(self):
        repo = DealRepositoryMock()

        response = repo.get_deal_by_id("00000000-0000-0000-0000-000000000000", "00000000-0000-0000-0000-000000000000")

        assert response.deal_id == "00000000-0000-0000-0000-000000000000"
        assert response.entity_id == "00000000-0000-0000-0000-000000000000"
        assert response.baseline == 1
        assert response.cpa == 1
        assert response.rev_share == 1
        assert response.conditions == "1"
        assert response.deal_status == DEAL_STATUS.ACTIVATED
        assert response.created_at == 1
        assert response.updated_at == 1

    def test_get_all_active_deals(self):
        repo = DealRepositoryMock()

        response = repo.get_all_active_deals()

        assert len(response) == 1
    
    def test_get_all_deals(self):
        repo = DealRepositoryMock()

        response = repo.get_all_deals()

        assert len(response) == 2
    
    def test_update_deal(self):
        repo = DealRepositoryMock()

        update_deal = Deal(
            deal_id="00000000-0000-0000-0000-000000000000",
            entity_id="00000000-0000-0000-0000-000000000000",
            baseline=2,
            cpa=2,
            rev_share=2,
            conditions="1",
            deal_status=DEAL_STATUS.ACTIVATED,
            created_at=2,
            updated_at=2,
        )

        response = repo.update_deal("00000000-0000-0000-0000-000000000000", update_deal)

        assert response.deal_id == "00000000-0000-0000-0000-000000000000"
        assert response.entity_id == "00000000-0000-0000-0000-000000000000"
        assert response.baseline == 2
        assert response.cpa == 2
        assert response.rev_share == 2
        assert response.conditions == "1"
        assert response.deal_status == DEAL_STATUS.ACTIVATED
        assert response.created_at == 2
        assert response.updated_at == 2
    
    def test_delete_deal(self):
        repo = DealRepositoryMock()

        repo.delete_deal(entity_id="00000000-0000-0000-0000-000000000000", deal_id="00000000-0000-0000-0000-000000000000")

        assert len(repo.deals) == 1