# classic_strategy.py
# 策略模式（Strategy pattern）—— 经典实现

"""
# tag::CLASSIC_STRATEGY_TESTS[]

    >>> joe = Customer('John Doe', 0)  # <1>
    >>> ann = Customer('Ann Smith', 1100)
    >>> cart = [LineItem('banana', 4, .5),  # <2>
    ...         LineItem('apple', 10, 1.5),
    ...         LineItem('watermelon', 5, 5.0)]
    >>> Order(joe, cart, FidelityPromo())  # <3>
    <Order total: 42.00 due: 42.00>
    >>> Order(ann, cart, FidelityPromo())  # <4>
    <Order total: 42.00 due: 39.90>
    >>> banana_cart = [LineItem('banana', 30, .5),  # <5>
    ...                LineItem('apple', 10, 1.5)]
    >>> Order(joe, banana_cart, BulkItemPromo())  # <6>
    <Order total: 30.00 due: 28.50>
    >>> long_cart = [LineItem(str(item_code), 1, 1.0) # <7>
    ...               for item_code in range(10)]
    >>> Order(joe, long_cart, LargeOrderPromo())  # <8>
    <Order total: 10.00 due: 9.30>
    >>> Order(joe, cart, LargeOrderPromo())
    <Order total: 42.00 due: 42.00>

# end::CLASSIC_STRATEGY_TESTS[]
"""
# tag::CLASSIC_STRATEGY[]

from abc import ABC, abstractmethod
import typing

from pytypes import typelogged

class Customer(typing.NamedTuple):
    name: str
    fidelity: int

@typelogged
class LineItem:

    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity


@typelogged
class Order:  # 上下文（Context）

    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion.discount(self)
        return self.total() - discount

    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())


@typelogged
class Promotion(ABC):  # 策略（Strategy）：一个抽象基类（abstract base class）

    @abstractmethod
    def discount(self, order):
        """返回折扣金额（正数，以美元计）"""


@typelogged
class FidelityPromo(Promotion):  # 第一个具体策略（Concrete Strategy）
    """为积分达到 1000 及以上的顾客提供 5% 折扣"""

    def discount(self, order):
        return order.total() * .05 if order.customer.fidelity >= 1000 else 0


@typelogged
class BulkItemPromo(Promotion):  # 第二个具体策略
    """为单项数量达到 20 及以上的 LineItem 提供 10% 折扣"""

    def discount(self, order):
        discount = 0
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total() * .1
        return discount


@typelogged
class LargeOrderPromo(Promotion):  # 第三个具体策略
    """为含 10 个及以上不同商品的订单提供 7% 折扣"""

    def discount(self, order):
        distinct_items = {item.product for item in order.cart}
        if len(distinct_items) >= 10:
            return order.total() * .07
        return 0

# end::CLASSIC_STRATEGY[]
