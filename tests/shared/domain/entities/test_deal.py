import pytest
from src.shared.domain.entities.deal import Deal
from src.shared.domain.enums.deal_status_enum import DEAL_STATUS


class Test_Deal:

    def test_deal(self):
        deal = Deal(deal_id="00000000-0000-0000-0000-000000000000", entity_id="00000000-0000-0000-0000-000000000000", baseline=1, cpa=1, rev_share=1, conditions="1", deal_status=DEAL_STATUS.ACTIVATED, created_at=1, updated_at=1)

        assert deal.deal_id == "00000000-0000-0000-0000-000000000000"
        assert deal.entity_id == "00000000-0000-0000-0000-000000000000"
        assert deal.baseline == 1
        assert deal.cpa == 1
        assert deal.rev_share == 1
        assert deal.conditions == "1"
        assert deal.deal_status == DEAL_STATUS.ACTIVATED
        assert deal.created_at == 1
        assert deal.updated_at == 1
    
    def test_deal_id_not_string(self):
        with pytest.raises(ValueError):
            Deal(deal_id=1, entity_id="00000000-0000-0000-0000-000000000000", baseline=1, cpa=1, rev_share=1, conditions="1", deal_status="1", created_at=1, updated_at=1)

    def test_deal_id_not_36_characters(self):
        with pytest.raises(ValueError):
            Deal(deal_id="1", entity_id="00000000-0000-0000-0000-000000000000", baseline=1, cpa=1, rev_share=1, conditions="1", deal_status="1", created_at=1, updated_at=1)

    def test_entity_id_not_string(self):
        with pytest.raises(ValueError):
            Deal(deal_id="00000000-0000-0000-0000-000000000000", entity_id=1, baseline=1, cpa=1, rev_share=1, conditions="1", deal_status="1", created_at=1, updated_at=1)

    def test_entity_id_not_36_characters(self):
        with pytest.raises(ValueError):
            Deal(deal_id="00000000-0000-0000-0000-000000000000", entity_id="1", baseline=1, cpa=1, rev_share=1, conditions="1", deal_status="1", created_at=1, updated_at=1)

    def test_baseline_not_float(self):
        with pytest.raises(ValueError):
            Deal(deal_id="00000000-0000-0000-0000-000000000000", entity_id="00000000-0000-0000-0000-000000000000", baseline="not_a_float", cpa=1, rev_share=1, conditions="1", deal_status="1", created_at=1, updated_at=1)

    def test_cpa_not_float(self):
        with pytest.raises(ValueError):
            Deal(deal_id="00000000-0000-0000-0000-000000000000", entity_id="00000000-0000-0000-0000-000000000000", baseline=1, cpa="not_a_float", rev_share=1, conditions="1", deal_status="1", created_at=1, updated_at=1)

    def test_rev_share_not_float(self):
        with pytest.raises(ValueError):
            Deal(deal_id="00000000-0000-0000-0000-000000000000", entity_id="00000000-0000-0000-0000-000000000000", baseline=1, cpa=1, rev_share="not_a_float", conditions="1", deal_status="1", created_at=1, updated_at=1)

    def test_conditions_not_string(self):
        with pytest.raises(ValueError):
            Deal(deal_id="00000000-0000-0000-0000-000000000000", entity_id="00000000-0000-0000-0000-000000000000", baseline=1, cpa=1, rev_share=1, conditions=1, deal_status="1", created_at=1, updated_at=1)

    def test_deal_status_invalid(self):
        with pytest.raises(ValueError):
            Deal(deal_id="00000000-0000-0000-0000-000000000000", entity_id="00000000-0000-0000-0000-000000000000", baseline=1, cpa=1, rev_share=1, conditions="1", deal_status="INVALID", created_at=1, updated_at=1)

    def test_created_at_not_integer(self):
        with pytest.raises(ValueError):
            Deal(deal_id="00000000-0000-0000-0000-000000000000", entity_id="00000000-0000-0000-0000-000000000000", baseline=1, cpa=1, rev_share=1, conditions="1", deal_status=DEAL_STATUS.ACTIVATED, created_at="not_an_int", updated_at=1)

    def test_updated_at_not_integer(self):
        with pytest.raises(ValueError):
            Deal(deal_id="00000000-0000-0000-0000-000000000000", entity_id="00000000-0000-0000-0000-000000000000", baseline=1, cpa=1, rev_share=1, conditions="1", deal_status=DEAL_STATUS.ACTIVATED, created_at=1, updated_at="not_an_int")

    def test_created_at_negative(self):
        with pytest.raises(ValueError):
            Deal(deal_id="00000000-0000-0000-0000-000000000000", entity_id="00000000-0000-0000-0000-000000000000", baseline=1, cpa=1, rev_share=1, conditions="1", deal_status=DEAL_STATUS.ACTIVATED, created_at=-1, updated_at=1)

    def test_updated_at_negative(self):
        with pytest.raises(ValueError):
            Deal(deal_id="00000000-0000-0000-0000-000000000000", entity_id="00000000-0000-0000-0000-000000000000", baseline=1, cpa=1, rev_share=1, conditions="1", deal_status=DEAL_STATUS.ACTIVATED, created_at=1, updated_at=-1)


    def test_to_dict(self):
        deal = Deal(deal_id="00000000-0000-0000-0000-000000000000", entity_id="00000000-0000-0000-0000-000000000000", baseline=1, cpa=1, rev_share=1, conditions="1", deal_status=DEAL_STATUS.ACTIVATED, created_at=1, updated_at=1)
        expected = {
            "deal_id": "00000000-0000-0000-0000-000000000000",
            "entity_id": "00000000-0000-0000-0000-000000000000",
            "baseline": 1,
            "cpa": 1,
            "rev_share": 1,
            "conditions": "1",
            "deal_status": "ACTIVATED",
            "created_at": 1,
            "updated_at": 1
        }

        assert deal.to_dict() == expected

    def test_from_dict(self):
        deal_dict = {
            "deal_id": "00000000-0000-0000-0000-000000000000",
            "entity_id": "00000000-0000-0000-0000-000000000000",
            "baseline": 1,
            "cpa": 1,
            "rev_share": 1,
            "conditions": "1",
            "deal_status": "ACTIVATED",
            "created_at": 1,
            "updated_at": 1
        }

        deal = Deal.from_dict(deal_dict)

        assert deal.deal_id == "00000000-0000-0000-0000-000000000000"
        assert deal.entity_id == "00000000-0000-0000-0000-000000000000"
        assert deal.baseline == 1
        assert deal.cpa == 1
        assert deal.rev_share == 1
        assert deal.conditions == "1"
        assert deal.deal_status == DEAL_STATUS.ACTIVATED
        assert deal.created_at == 1
        assert deal.updated_at == 1