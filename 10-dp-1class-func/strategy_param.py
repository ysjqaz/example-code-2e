# strategy_param.py
# 策略模式（Strategy pattern）—— 用闭包（closure）参数化

"""
    >>> joe = Customer('John Doe', 0)
    >>> ann = Customer('Ann Smith', 1100)
    >>> cart = [LineItem('banana', 4, .5),
    ...         LineItem('apple', 10, 1.5),
    ...         LineItem('watermelon', 5, 5.0)]
    >>> Order(joe, cart, fidelity_promo(10))
    <Order total: 42.00 due: 42.00>
    >>> Order(ann, cart, fidelity_promo(10))
    <Order total: 42.00 due: 37.80>
    >>> banana_cart = [LineItem('banana', 30, .5),
    ...                LineItem('apple', 10, 1.5)]
    >>> Order(joe, banana_cart, bulk_item_promo(10))
    <Order total: 30.00 due: 28.50>
    >>> long_cart = [LineItem(str(item_code), 1, 1.0)
    ...               for item_code in range(10)]
    >>> Order(joe, long_cart, LargeOrderPromo(7))
    <Order total: 10.00 due: 9.30>
    >>> Order(joe, cart, LargeOrderPromo(7))
    <Order total: 42.00 due: 42.00>

使用 ``partial`` 即时构建一个参数化的折扣器::

    >>> from functools import partial
    >>> Order(joe, cart, partial(general_discount, 5))
    <Order total: 42.00 due: 39.90>

"""

import typing
from typing import Sequence, Optional, Callable


class Customer(typing.NamedTuple):
    name: str
    fidelity: int


class LineItem:
    def __init__(self, product: str, quantity: int, price: float):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity


class Order:  # 上下文（Context）
    def __init__(
        self,
        customer: Customer,
        cart: Sequence[LineItem],
        promotion: Optional['Promotion'] = None,
    ):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion

    def total(self) -> float:
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self) -> float:
        if self.promotion is None:
            discount = 0.0
        else:
            discount = self.promotion(self)  # <1>
        return self.total() - discount

    def __repr__(self):
        return f'<Order total: {self.total():.2f} due: {self.due():.2f}>'


# tag::STRATEGY_PARAM[]

Promotion = Callable[[Order], float]  # <2>


def fidelity_promo(percent: float) -> Promotion:
    """为积分达到 1000 及以上的顾客提供折扣"""
    return lambda order: (
        order.total() * percent / 100 if order.customer.fidelity >= 1000 else 0
    )


def bulk_item_promo(percent: float) -> Promotion:
    """为单项数量达到 20 及以上的 LineItem 提供折扣"""

    def discounter(order: Order) -> float:
        discount = 0
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total() * percent / 100
        return discount

    return discounter


class LargeOrderPromo:
    """为含 10 个及以上不同商品的订单提供折扣"""

    def __init__(self, percent: float):
        self.percent = percent

    def __call__(self, order: Order) -> float:
        distinct_items = {item.product for item in order.cart}
        if len(distinct_items) >= 10:
            return order.total() * self.percent / 100
        return 0


def general_discount(percent: float, order: Order) -> float:
    """无限制折扣；用法：``partial(general_discount, 5)``"""
    return order.total() * percent / 100


# end::STRATEGY[]
