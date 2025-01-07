from typing import List
from src.shared.domain.entities.deal import Deal
from src.shared.domain.enums.deal_status_enum import DEAL_STATUS
from src.shared.domain.repositories.deal_repository_interface import IDealRepository


class DealRepositoryMock(IDealRepository):
    deals: List[Deal]

    def __init__(self):
        self.deals = [
            Deal(
                deal_id="00000000-0000-0000-0000-000000000000",
                bet_id="00000000-0000-0000-0000-000000000000",
                baseline=1,
                cpa=1,
                rev_share=1,
                conditions="1",
                deal_status=DEAL_STATUS.ACTIVATED,
                created_at=1,
                updated_at=1,
            ),
            Deal(
                deal_id="00000000-0000-0000-0000-000000000001",
                bet_id="00000000-0000-0000-0000-000000000001",
                baseline=1,
                cpa=1,
                rev_share=1,
                conditions="1",
                deal_status=DEAL_STATUS.DEACTIVATED,
                created_at=1,
                updated_at=1,
            ),
        ]

    def create_deal(self, deal: Deal) -> Deal:
        self.deals.append(deal)
        return deal
    
    def get_deal_by_id(self, bet_id: str, deal_id: str) -> Deal:
        for deal in self.deals:
            if deal.bet_id == bet_id and deal.deal_id == deal_id:
                return deal
        
        return None
    
    def get_all_active_deals(self) -> List[Deal]:
        active_deals = []

        for deal in self.deals:
            if deal.deal_status == DEAL_STATUS.ACTIVATED:
                active_deals.append(deal)

        return active_deals
    
    def get_all_deals(self) -> List[Deal]:
        return self.deals
    
    def update_deal(self, deal_id: str, new_deal: Deal) -> Deal:
        for deal in self.deals:
            if deal.deal_id == deal_id:
                deal.bet_id = new_deal.bet_id
                deal.baseline = new_deal.baseline
                deal.cpa = new_deal.cpa
                deal.rev_share = new_deal.rev_share
                deal.conditions = new_deal.conditions
                deal.deal_status = new_deal.deal_status
                deal.created_at = new_deal.created_at
                deal.updated_at = new_deal.updated_at
                return deal
        
        return None
    
    def delete_deal(self, bet_id: str, deal_id: str) -> Deal:
        for deal in self.deals:
            if deal.bet_id == bet_id and deal.deal_id == deal_id:
                self.deals.remove(deal)
                return deal
        
        return None
    