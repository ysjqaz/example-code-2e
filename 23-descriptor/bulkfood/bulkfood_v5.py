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

未做任何更改::

    >>> raisins.weight
    10

价格为负数或 0 同样不可接受::

    >>> truffle = LineItem('White truffle', 100, 0)
    Traceback (most recent call last):
        ...
    ValueError: price must be > 0

如果在类上访问该描述符，会返回描述符对象本身:

    >>> LineItem.weight  # doctest: +ELLIPSIS
    <model_v5.Quantity object at 0x...>
    >>> LineItem.weight.storage_name
    'weight'

`NonBlank` 描述符防止用空字符串或全空白字符串作为 description:

    >>> br_nuts = LineItem('Brazil Nuts', 10, 34.95)
    >>> br_nuts.description = ' '
    Traceback (most recent call last):
        ...
    ValueError: description cannot be blank
    >>> void = LineItem('', 1, 1)
    Traceback (most recent call last):
        ...
    ValueError: description cannot be blank


"""

# tag::LINEITEM_V5[]
import model_v5 as model  # <1>

class LineItem:
    description = model.NonBlank()  # <2>
    weight = model.Quantity()
    price = model.Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price
# end::LINEITEM_V5[]
