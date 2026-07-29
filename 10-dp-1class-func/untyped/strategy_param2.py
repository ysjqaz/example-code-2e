# strategy_param2.py
# 策略模式（Strategy pattern）—— 用可调用对象（callable）参数化

"""
    >>> joe = Customer('John Doe', 0)
    >>> ann = Customer('Ann Smith', 1100)
    >>> cart = [LineItem('banana', 4, .5),
    ...         LineItem('apple', 10, 1.5),
    ...         LineItem('watermelon', 5, 5.0)]
    >>> Order(joe, cart, FidelityPromo(10))
    <Order total: 42.00 due: 42.00>
    >>> Order(ann, cart, FidelityPromo(10))
    <Order total: 42.00 due: 37.80>
    >>> banana_cart = [LineItem('banana', 30, .5),
    ...                LineItem('apple', 10, 1.5)]
    >>> Order(joe, banana_cart, BulkItemPromo(10))
    <Order total: 30.00 due: 28.50>
    >>> long_cart = [LineItem(str(item_code), 1, 1.0)
    ...               for item_code in range(10)]
    >>> Order(joe, long_cart, LargeOrderPromo(7))
    <Order total: 10.00 due: 9.30>
    >>> Order(joe, cart, LargeOrderPromo(7))
    <Order total: 42.00 due: 42.00>

"""

from collections import namedtuple

Customer = namedtuple('Customer', 'name fidelity')


class LineItem:

    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity


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
            discount = self.promotion(self)  # <1>
        return self.total() - discount

    def __repr__(self):
        return f'<Order total: {self.total():.2f} due: {self.due():.2f}>'


class Promotion:
    """计算订单折扣"""

    def __init__(self, percent):
        self.percent = percent

    def __call__(self, order):
        raise NotImplementedError("Subclass responsibility")


class FidelityPromo(Promotion):
    """为积分达到 1000 及以上的顾客提供折扣"""

    def __call__(self, order):
        if order.customer.fidelity >= 1000:
            return order.total() * self.percent / 100
        return 0


class BulkItemPromo(Promotion):
    """为单项数量达到 20 及以上的 LineItem 提供折扣"""

    def __call__(self, order):
        discount = 0
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total() * self.percent / 100
        return discount


class LargeOrderPromo(Promotion):
    """为含 10 个及以上不同商品的订单提供折扣"""

    def __call__(self, order):
        distinct_items = {item.product for item in order.cart}
        if len(distinct_items) >= 10:
            return order.total() * self.percent / 100
        return 0
