from concurrent.futures import ThreadPoolExecutor

import pytest

from shop.inventory import Inventory, OutOfStock


def test_reserve_decrements_stock():
    inv = Inventory({"KB-01": 3})
    inv.reserve("KB-01", 2)
    assert inv.remaining("KB-01") == 1


def test_reserve_raises_when_insufficient():
    inv = Inventory({"KB-01": 1})
    with pytest.raises(OutOfStock):
        inv.reserve("KB-01", 2)


def test_concurrent_reserve_never_oversells():
    inv = Inventory({"KB-01": 100})
    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(lambda _: inv.reserve("KB-01", 1), range(100)))
    assert inv.remaining("KB-01") == 0
