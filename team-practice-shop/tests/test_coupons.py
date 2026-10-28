from decimal import Decimal

from shop.coupons import discount_for


def test_same_code_applies_once_per_order():
    assert discount_for(Decimal("100000"), ["VIP20", "VIP20"]) == Decimal("20000")


def test_min_subtotal_not_met():
    assert discount_for(Decimal("100000"), ["BULK15"]) == Decimal("0")


def test_unknown_code_is_ignored():
    assert discount_for(Decimal("100000"), ["NOPE"]) == Decimal("0")
