"""주문 처리와 배치 정산."""

import json
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path

from shop.catalog import unit_price
from shop.coupons import discount_for
from shop.inventory import Inventory
from shop.pricing import shipping_fee, to_won


@dataclass
class OrderLine:
    sku: str
    qty: int


@dataclass
class Order:
    order_id: str
    customer: str
    lines: list[OrderLine]
    coupon_codes: list[str] = field(default_factory=list)


@dataclass
class Receipt:
    order_id: str
    subtotal: Decimal
    discount: Decimal
    shipping: Decimal
    total: Decimal


def process_order(order: Order, inventory: Inventory) -> Receipt:
    subtotal = sum((unit_price(l.sku) * l.qty for l in order.lines), Decimal("0"))
    for line in order.lines:
        inventory.reserve(line.sku, line.qty)
    discount = to_won(discount_for(subtotal, order.coupon_codes))
    shipping = shipping_fee(subtotal - discount)
    total = subtotal - discount + shipping
    return Receipt(order.order_id, subtotal, discount, shipping, total)


def process_batch(
    orders: list[Order], inventory: Inventory, workers: int = 4
) -> dict[str, Receipt]:
    with ThreadPoolExecutor(max_workers=workers) as pool:
        receipts = pool.map(lambda o: process_order(o, inventory), orders)
    return {r.order_id: r for r in receipts}


def load_orders(path: Path) -> list[Order]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return [
        Order(
            order_id=o["order_id"],
            customer=o["customer"],
            lines=[OrderLine(l["sku"], l["qty"]) for l in o["lines"]],
            coupon_codes=o.get("coupon_codes", []),
        )
        for o in raw
    ]
