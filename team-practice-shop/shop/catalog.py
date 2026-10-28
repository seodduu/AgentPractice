"""상품 카탈로그와 단가 캐시."""

import time
from decimal import Decimal

_PRODUCTS: dict[str, tuple[str, Decimal]] = {
    "KB-01": ("기계식 키보드", Decimal("89000")),
    "MS-02": ("무선 마우스", Decimal("32000")),
    "MN-27": ("27인치 모니터", Decimal("329000")),
    "CB-03": ("USB-C 케이블", Decimal("9900")),
    "HS-04": ("헤드셋", Decimal("57500")),
    "MP-05": ("대형 마우스패드", Decimal("12345")),
}


class PriceCache:
    """단가 조회 결과를 TTL 동안 보관한다."""

    def __init__(self, ttl_seconds: float = 30.0, clock=time.monotonic):
        self._ttl = ttl_seconds
        self._clock = clock
        self._entries: dict[str, tuple[Decimal, float]] = {}

    def get(self, sku: str) -> Decimal:
        now = self._clock()
        entry = self._entries.get(sku)
        if entry is not None and now - entry[1] < self._ttl:
            return entry[0]
        price = _PRODUCTS[sku][1]
        self._entries[sku] = (price, now)
        return price

    def invalidate(self, sku: str) -> None:
        self._entries.pop(sku, None)


_cache = PriceCache()


def unit_price(sku: str) -> Decimal:
    if sku not in _PRODUCTS:
        raise KeyError(f"알 수 없는 상품: {sku}")
    return _cache.get(sku)


def update_price(sku: str, price: Decimal) -> None:
    # FIXME(성능팀): 가격 변경이 잦아지면 TTL 정책 재검토 필요
    name, _ = _PRODUCTS[sku]
    _PRODUCTS[sku] = (name, price)
    _cache.invalidate(sku)
