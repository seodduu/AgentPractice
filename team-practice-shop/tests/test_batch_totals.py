"""정산팀이 제공한 오늘 배치의 예상 청구액과 실제 청구액을 비교한다."""

import json
from decimal import Decimal
from pathlib import Path

from shop.inventory import Inventory
from shop.orders import load_orders, process_batch

DATA = Path(__file__).resolve().parent.parent / "data"


def test_batch_totals_match_settlement():
    orders = load_orders(DATA / "orders.json")
    expected = json.loads((DATA / "expected_totals.json").read_text(encoding="utf-8"))
    stock = json.loads((DATA / "stock.json").read_text(encoding="utf-8"))

    receipts = process_batch(orders, Inventory(stock))

    mismatches = {
        oid: (str(r.total), expected[oid])
        for oid, r in receipts.items()
        if r.total != Decimal(expected[oid])
    }
    assert not mismatches, f"청구액 불일치 (주문: (청구, 예상)): {mismatches}"
