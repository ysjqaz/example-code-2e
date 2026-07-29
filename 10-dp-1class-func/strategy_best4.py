# strategy_best4.py
# 策略模式（Strategy pattern）—— 基于函数的实现
# 从由装饰器（decorator）注册的函数列表中选择最佳促销

"""
    >>> from decimal import Decimal
    >>> from strategy import Customer, LineItem, Order
    >>> from promotions import *
    >>> joe = Customer('John Doe', 0)
    >>> ann = Customer('Ann Smith', 1100)
    >>> cart = [LineItem('banana', 4, Decimal('.5')),
    ...         LineItem('apple', 10, Decimal('1.5')),
    ...         LineItem('watermelon', 5, Decimal(5))]
    >>> Order(joe, cart, fidelity_promo)
    <Order total: 42.00 due: 42.00>
    >>> Order(ann, cart, fidelity_promo)
    <Order total: 42.00 due: 39.90>
    >>> banana_cart = [LineItem('banana', 30, Decimal('.5')),
    ...                LineItem('apple', 10, Decimal('1.5'))]
    >>> Order(joe, banana_cart, bulk_item_promo)
    <Order total: 30.00 due: 28.50>
    >>> long_cart = [LineItem(str(item_code), 1, Decimal(1))
    ...               for item_code in range(10)]
    >>> Order(joe, long_cart, large_order_promo)
    <Order total: 10.00 due: 9.30>
    >>> Order(joe, cart, large_order_promo)
    <Order total: 42.00 due: 42.00>

# tag::STRATEGY_BEST_TESTS[]

    >>> Order(joe, long_cart, best_promo)
    <Order total: 10.00 due: 9.30>
    >>> Order(joe, banana_cart, best_promo)
    <Order total: 30.00 due: 28.50>
    >>> Order(ann, cart, best_promo)
    <Order total: 42.00 due: 39.90>

# end::STRATEGY_BEST_TESTS[]
"""

from decimal import Decimal
from typing import Callable

from strategy import Order

# tag::STRATEGY_BEST4[]

Promotion = Callable[[Order], Decimal]

promos: list[Promotion] = []  # <1>


def promotion(promo: Promotion) -> Promotion:  # <2>
    promos.append(promo)
    return promo


def best_promo(order: Order) -> Decimal:
    """计算可用的最佳折扣"""
    return max(promo(order) for promo in promos)  # <3>


@promotion  # <4>
def fidelity(order: Order) -> Decimal:
    """为积分达到 1000 及以上的顾客提供 5% 折扣"""
    if order.customer.fidelity >= 1000:
        return order.total() * Decimal('0.05')
    return Decimal(0)


@promotion
def bulk_item(order: Order) -> Decimal:
    """为单项数量达到 20 及以上的 LineItem 提供 10% 折扣"""
    discount = Decimal(0)
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * Decimal('0.1')
    return discount


@promotion
def large_order(order: Order) -> Decimal:
    """为含 10 个及以上不同商品的订单提供 7% 折扣"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * Decimal('0.07')
    return Decimal(0)

# end::STRATEGY_BEST4[]
