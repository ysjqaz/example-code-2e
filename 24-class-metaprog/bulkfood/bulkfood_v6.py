"""

散装食品订单中的一个明细项（line item）包含 description、weight 和 price 字段::

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

没有发生改变::

    >>> raisins.weight
    10

由描述符（descriptor）管理的属性，其值存放在备选属性里；
这些备选属性由描述符在每个 ``LineItem`` 实例（instance）上创建::

# tag::LINEITEM_V6_DEMO[]
    >>> raisins = LineItem('Golden raisins', 10, 6.95)
    >>> dir(raisins)[:3]
    ['_NonBlank#description', '_Quantity#price', '_Quantity#weight']
    >>> LineItem.description.storage_name
    '_NonBlank#description'
    >>> raisins.description
    'Golden raisins'
    >>> getattr(raisins, '_NonBlank#description')
    'Golden raisins'

# end::LINEITEM_V6_DEMO[]

如果在类上访问描述符，返回的是描述符对象本身：

    >>> LineItem.weight  # doctest: +ELLIPSIS
    <model_v6.Quantity object at 0x...>
    >>> LineItem.weight.storage_name
    '_Quantity#weight'


`NonBlank` 描述符禁止把空字符串或全空白字符串用作 description：

    >>> br_nuts = LineItem('Brazil Nuts', 10, 34.95)
    >>> br_nuts.description = ' '
    Traceback (most recent call last):
        ...
    ValueError: value cannot be empty or blank
    >>> void = LineItem('', 1, 1)
    Traceback (most recent call last):
        ...
    ValueError: value cannot be empty or blank


"""

# tag::LINEITEM_V6[]
import model_v6 as model

@model.entity  # <1>
class LineItem:
    description = model.NonBlank()
    weight = model.Quantity()
    price = model.Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price
# end::LINEITEM_V6[]
