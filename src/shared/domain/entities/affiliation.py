from typing import Optional
from src.shared.helpers.errors.errors import EntityError


class Affiliation:
    def __init__(
        self,
        affiliation_id: str,
        invoiced_amount: float,
        amount_to_pay: float,
        commission: float,
        baseline: float,
        cost_per_acquisition: int,
        rev_share: float,
        registers: int,
        ftd: int,
        shipping_volume: float,
        base_quality: float,
        operators_satisfaction: float,
    ):
        self._validate_affiliation(
            affiliation_id,
            invoiced_amount,
            amount_to_pay,
            commission,
            baseline,
            cost_per_acquisition,
            rev_share,
            registers,
            ftd,
            shipping_volume,
            base_quality,
            operators_satisfaction,
        )

        self.affiliation_id = affiliation_id
        self.invoiced_amount = invoiced_amount
        self.amount_to_pay = amount_to_pay
        self.commission = commission
        self.baseline = baseline
        self.cost_per_acquisition = cost_per_acquisition
        self.rev_share = rev_share
        self.registers = registers
        self.ftd = ftd
        self.shipping_volume = shipping_volume
        self.base_quality = base_quality
        self.operators_satisfaction = operators_satisfaction

    @staticmethod
    def _validate_affiliation(
        affiliation_id: str,
        invoiced_amount: float,
        amount_to_pay: float,
        commission: float,
        baseline: float,
        cost_per_acquisition: int,
        rev_share: float,
        registers: int,
        ftd: int,
        shipping_volume: float,
        base_quality: float,
        operators_satisfaction: float,
    ):
        if not affiliation_id:
            raise EntityError("Affiliation ID is required")
        if invoiced_amount < 0:
            raise EntityError("Invoiced amount must be a positive number")
        if amount_to_pay < 0:
            raise EntityError("Amount to pay must be a positive number")
        if commission < 0:
            raise EntityError("Commission must be a positive number")
        if baseline < 0:
            raise EntityError("Baseline must be a positive number")
        if cost_per_acquisition < 0:
            raise EntityError("Cost per acquisition must be a positive integer")
        if rev_share < 0 or rev_share > 1:
            raise EntityError("Rev share must be a float between 0 and 1")
        if registers < 0:
            raise EntityError("Registers must be a positive integer")
        if ftd < 0:
            raise EntityError("FTD must be a positive integer")
        if shipping_volume < 0:
            raise EntityError("Shipping volume must be a positive number")
        if base_quality < 0 or base_quality > 100:
            raise EntityError("Base quality must be a percentage between 0 and 100")
        if operators_satisfaction < 0 or operators_satisfaction > 100:
            raise EntityError(
                "Operators satisfaction must be a percentage between 0 and 100"
            )

    def to_dict(self) -> dict:
        return {
            "affiliation_id": self.affiliation_id,
            "invoiced_amount": self.invoiced_amount,
            "amount_to_pay": self.amount_to_pay,
            "commission": self.commission,
            "baseline": self.baseline,
            "cost_per_acquisition": self.cost_per_acquisition,
            "rev_share": self.rev_share,
            "registers": self.registers,
            "ftd": self.ftd,
            "shipping_volume": self.shipping_volume,
            "base_quality": self.base_quality,
            "operators_satisfaction": self.operators_satisfaction,
        }
