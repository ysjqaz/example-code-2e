"""
散装食品订单中的一个明细项（line item），包含 description、weight 和 price 字段。
``subtotal`` 方法返回该明细项的总价::

    >>> raisins = LineItem('Golden raisins', 10, 6.95)
    >>> raisins.weight, raisins.description, raisins.price
    (10, 'Golden raisins', 6.95)
    >>> raisins.subtotal()
    69.5

但是，没有校验的话，这些公开属性（attribute）可能惹出麻烦::

# tag::LINEITEM_PROBLEM_V1[]

    >>> raisins = LineItem('Golden raisins', 10, 6.95)
    >>> raisins.subtotal()
    69.5
    >>> raisins.weight = -20  # garbage in...
    >>> raisins.subtotal()    # garbage out...
    -139.0

# end::LINEITEM_PROBLEM_V1[]

"""


# tag::LINEITEM_V1[]
class LineItem:

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price
# end::LINEITEM_V1[]
