from decimal import Decimal

from shop import catalog
from shop.catalog import PriceCache


def test_cache_returns_cached_price_within_ttl():
    now = [0.0]
    cache = PriceCache(ttl_seconds=30, clock=lambda: now[0])
    assert cache.get("KB-01") == Decimal("89000")
    now[0] = 10.0
    assert cache.get("KB-01") == Decimal("89000")


def test_update_price_is_visible_immediately():
    original = catalog.unit_price("CB-03")
    try:
        catalog.update_price("CB-03", Decimal("8900"))
        assert catalog.unit_price("CB-03") == Decimal("8900")
    finally:
        catalog.update_price("CB-03", original)
