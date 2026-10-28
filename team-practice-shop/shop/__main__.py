"""오늘 배치를 돌려 정산 예상액과 비교한다. 실행: python -m shop"""

import json
from decimal import Decimal
from pathlib import Path

from shop.inventory import Inventory
from shop.orders import load_orders, process_batch

DATA = Path(__file__).resolve().parent.parent / "data"


def main() -> None:
    orders = load_orders(DATA / "orders.json")
    expected = json.loads((DATA / "expected_totals.json").read_text(encoding="utf-8"))
    stock = json.loads((DATA / "stock.json").read_text(encoding="utf-8"))
    receipts = process_batch(orders, Inventory(stock))

    mismatches = 0
    for order in orders:
        receipt = receipts[order.order_id]
        want = Decimal(expected[order.order_id])
        mark = "OK " if receipt.total == want else "불일치"
        if receipt.total != want:
            mismatches += 1
        print(f"[{mark}] {order.order_id}  청구 {receipt.total:>8}  정산 예상 {want:>8}")
    print(f"\n불일치 {mismatches}건 / 전체 {len(orders)}건")


if __name__ == "__main__":
    main()
