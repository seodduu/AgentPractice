from decimal import Decimal

from shop.pricing import shipping_fee, to_won


def test_to_won_rounds_half_up():
    assert to_won(Decimal("1234.5")) == Decimal("1235")
    assert to_won(Decimal("1234.4")) == Decimal("1234")


def test_shipping_fee_threshold():
    assert shipping_fee(Decimal("49999")) == Decimal("3000")
    assert shipping_fee(Decimal("50000")) == Decimal("0")
