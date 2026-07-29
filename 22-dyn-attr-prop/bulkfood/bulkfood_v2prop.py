"""

散装食品订单中的一个明细项（line item），包含 description、weight 和 price 字段::

    >>> raisins = LineItem('Golden raisins', 10, 6.95)
    >>> raisins.weight, raisins.description, raisins.price
    (10, 'Golden raisins', 6.95)

``subtotal`` 方法返回该明细项的总价::

    >>> raisins.subtotal()
    69.5

``LineItem`` 的 weight 必须大于 0::

    >>> raisins.weight = -20
    Traceback (most recent call last):
        ...
    ValueError: value must be > 0

未做任何修改::

    >>> raisins.weight
    10

由特性（property）所管理的属性值，存储在每个 ``LineItem`` 实例
中创建的实例属性里::

# tag::LINEITEM_V2_PROP_DEMO[]
    >>> nutmeg = LineItem('Moluccan nutmeg', 8, 13.95)
    >>> nutmeg.weight, nutmeg.price  # <1>
    (8, 13.95)
    >>> nutmeg.__dict__  # <2>
    {'description': 'Moluccan nutmeg', 'weight': 8, 'price': 13.95}

# end::LINEITEM_V2_PROP_DEMO[]

"""


# tag::LINEITEM_V2_PROP_FACTORY_FUNCTION[]
def quantity(storage_name):  # <1>

    def qty_getter(instance):  # <2>
        return instance.__dict__[storage_name]  # <3>

    def qty_setter(instance, value):  # <4>
        if value > 0:
            instance.__dict__[storage_name] = value  # <5>
        else:
            raise ValueError('value must be > 0')

    return property(qty_getter, qty_setter)  # <6>
# end::LINEITEM_V2_PROP_FACTORY_FUNCTION[]


# tag::LINEITEM_V2_PROP_CLASS[]
class LineItem:
    weight = quantity('weight')  # <1>
    price = quantity('price')  # <2>

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight  # <3>
        self.price = price

    def subtotal(self):
        return self.weight * self.price  # <4>
# end::LINEITEM_V2_PROP_CLASS[]
