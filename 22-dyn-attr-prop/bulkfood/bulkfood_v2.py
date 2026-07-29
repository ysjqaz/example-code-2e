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

实例化时也会执行该校验::

    >>> walnuts = LineItem('walnuts', 0, 10.00)
    Traceback (most recent call last):
        ...
    ValueError: value must be > 0

如有需要——例如白盒测试——仍然可以访问这个受保护属性（protected attribute）::

    >>> raisins._LineItem__weight
    10

"""


# tag::LINEITEM_V2[]
class LineItem:

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight  # <1>
        self.price = price

    def subtotal(self):
        return self.weight * self.price

    @property  # <2>
    def weight(self):  # <3>
        return self.__weight  # <4>

    @weight.setter  # <5>
    def weight(self, value):
        if value > 0:
            self.__weight = value  # <6>
        else:
            raise ValueError('value must be > 0')  # <7>
# end::LINEITEM_V2[]
