"""

散装食品订单中的一个行项目有 description、weight 和 price 字段::

    >>> raisins = LineItem('Golden raisins', 10, 6.95)
    >>> raisins.weight, raisins.description, raisins.price
    (10, 'Golden raisins', 6.95)

``subtotal`` 方法给出该行项目的总价::

    >>> raisins.subtotal()
    69.5

``LineItem`` 的 weight 必须大于 0::

    >>> raisins.weight = -20
    Traceback (most recent call last):
        ...
    ValueError: weight must be > 0

价格为负数或 0 同样不可接受::

    >>> truffle = LineItem('White truffle', 100, 0)
    Traceback (most recent call last):
        ...
    ValueError: price must be > 0

未做任何更改::

    >>> raisins.weight
    10

"""


# tag::LINEITEM_QUANTITY_V3[]
class Quantity:  # <1>

    def __init__(self, storage_name):
        self.storage_name = storage_name  # <2>

    def __set__(self, instance, value):  # <3>
        if value > 0:
            instance.__dict__[self.storage_name] = value  # <4>
        else:
            msg = f'{self.storage_name} must be > 0'
            raise ValueError(msg)

    def __get__(self, instance, owner):  # <5>
        return instance.__dict__[self.storage_name]


# end::LINEITEM_QUANTITY_V3[]

# tag::LINEITEM_V3[]
class LineItem:
    weight = Quantity('weight')  # <1>
    price = Quantity('price')  # <2>

    def __init__(self, description, weight, price):  # <3>
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price
# end::LINEITEM_V3[]
