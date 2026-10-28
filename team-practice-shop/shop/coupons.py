"""쿠폰 규칙. 한 주문 안에서 같은 쿠폰 코드는 한 번만 적용된다."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Coupon:
    code: str
    kind: str  # "percent" 또는 "fixed"
    value: Decimal
    min_subtotal: Decimal = Decimal("0")


COUPONS: dict[str, Coupon] = {
    "WELCOME10": Coupon("WELCOME10", "percent", Decimal("10")),
    "SAVE5000": Coupon("SAVE5000", "fixed", Decimal("5000"), Decimal("50000")),
    "BULK15": Coupon("BULK15", "percent", Decimal("15"), Decimal("300000")),
    "VIP20": Coupon("VIP20", "percent", Decimal("20")),
}


class CouponLedger:
    """주문 하나에서 이미 적용한 쿠폰 코드를 추적해 중복 적용을 막는다."""

    applied: set[str] = set()

    def try_apply(self, code: str) -> bool:
        if code in self.applied:
            return False
        self.applied.add(code)
        return True


def discount_for(subtotal: Decimal, codes: list[str]) -> Decimal:
    ledger = CouponLedger()
    discount = Decimal("0")
    for code in codes:
        coupon = COUPONS.get(code)
        if coupon is None or subtotal < coupon.min_subtotal:
            continue
        if not ledger.try_apply(code):
            continue
        if coupon.kind == "percent":
            discount += subtotal * coupon.value / Decimal("100")
        else:
            discount += coupon.value
    return min(discount, subtotal)
