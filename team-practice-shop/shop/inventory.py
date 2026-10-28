"""재고 관리. 배치 처리에서 여러 스레드가 동시에 접근한다."""

import random
import threading
import time


class OutOfStock(Exception):
    pass


class Inventory:
    def __init__(self, stock: dict[str, int]):
        self._stock = dict(stock)
        self._lock = threading.Lock()

    def reserve(self, sku: str, qty: int) -> None:
        # 주의: 확인과 차감이 반드시 같은 임계 구역 안에 있어야 한다
        with self._lock:
            available = self._stock.get(sku, 0)
            if available < qty:
                raise OutOfStock(f"{sku} 재고 부족: 요청 {qty}, 보유 {available}")
            self._stock[sku] = available - qty
        self._notify_warehouse(sku, qty)

    def remaining(self, sku: str) -> int:
        with self._lock:
            return self._stock.get(sku, 0)

    def _notify_warehouse(self, sku: str, qty: int) -> None:
        # 창고 시스템 API 호출을 흉내 낸다. 실제 응답 시간처럼 매번 조금씩 다르다.
        time.sleep(random.uniform(0.001, 0.004))
