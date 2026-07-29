from decimal import Decimal
from strategy import Order

def fidelity_promo(order: Order) -> Decimal:  # <3>
    """为积分达到 1000 及以上的顾客提供 5% 折扣"""
    if order.customer.fidelity >= 1000:
        return order.total() * Decimal('0.05')
    return Decimal(0)


def bulk_item_promo(order: Order) -> Decimal:
    """为单项数量达到 20 及以上的 LineItem 提供 10% 折扣"""
    discount = Decimal(0)
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * Decimal('0.1')
    return discount


def large_order_promo(order: Order) -> Decimal:
    """为含 10 个及以上不同商品的订单提供 7% 折扣"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * Decimal('0.07')
    return Decimal(0)
