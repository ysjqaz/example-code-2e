# strategy_best.py
# 策略模式（Strategy pattern）—— 基于函数的实现
# 从静态函数列表中选择最佳促销

"""
    >>> joe = Customer('John Doe', 0)
    >>> ann = Customer('Ann Smith', 1100)
    >>> cart = [LineItem('banana', 4, .5),
    ...         LineItem('apple', 10, 1.5),
    ...         LineItem('watermelon', 5, 5.0)]
    >>> Order(joe, cart, fidelity_promo)
    <Order total: 42.00 due: 42.00>
    >>> Order(ann, cart, fidelity_promo)
    <Order total: 42.00 due: 39.90>
    >>> banana_cart = [LineItem('banana', 30, .5),
    ...                LineItem('apple', 10, 1.5)]
    >>> Order(joe, banana_cart, bulk_item_promo)
    <Order total: 30.00 due: 28.50>
    >>> long_cart = [LineItem(str(item_code), 1, 1.0)
    ...               for item_code in range(10)]
    >>> Order(joe, long_cart, large_order_promo)
    <Order total: 10.00 due: 9.30>
    >>> Order(joe, cart, large_order_promo)
    <Order total: 42.00 due: 42.00>

# tag::STRATEGY_BEST_TESTS[]

    >>> Order(joe, long_cart, best_promo)  # <1>
    <Order total: 10.00 due: 9.30>
    >>> Order(joe, banana_cart, best_promo)  # <2>
    <Order total: 30.00 due: 28.50>
    >>> Order(ann, cart, best_promo)  # <3>
    <Order total: 42.00 due: 39.90>

# end::STRATEGY_BEST_TESTS[]
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
            discount = self.promotion(self)
        return self.total() - discount

    def __repr__(self):
        return f'<Order total: {self.total():.2f} due: {self.due():.2f}>'


def fidelity_promo(order):
    """为积分达到 1000 及以上的顾客提供 5% 折扣"""
    return order.total() * .05 if order.customer.fidelity >= 1000 else 0


def bulk_item_promo(order):
    """为单项数量达到 20 及以上的 LineItem 提供 10% 折扣"""
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * .1
    return discount


def large_order_promo(order):
    """为含 10 个及以上不同商品的订单提供 7% 折扣"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * .07
    return 0

# tag::STRATEGY_BEST[]

promos = [fidelity_promo, bulk_item_promo, large_order_promo]  # <1>

def best_promo(order):  # <2>
    """选择可用的最佳折扣
    """
    return max(promo(order) for promo in promos)  # <3>

# end::STRATEGY_BEST[]
