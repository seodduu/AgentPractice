"""금액 계산 규칙. 모든 금액은 원 단위 Decimal 로 다룬다."""

from decimal import ROUND_HALF_UP, Decimal

FREE_SHIPPING_THRESHOLD = Decimal("50000")
SHIPPING_FEE = Decimal("3000")


def to_won(amount: Decimal) -> Decimal:
    # TODO: 반올림 정책(사사오입 vs 은행가 반올림) 재무팀 최종 확인 필요
    return amount.quantize(Decimal("1"), rounding=ROUND_HALF_UP)


def shipping_fee(amount_after_discount: Decimal) -> Decimal:
    if amount_after_discount >= FREE_SHIPPING_THRESHOLD:
        return Decimal("0")
    return SHIPPING_FEE
