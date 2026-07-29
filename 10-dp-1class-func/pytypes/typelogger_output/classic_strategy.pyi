"""
自动生成的存根文件（stubfile），对应

/home/luciano/flupy/priv/2e-atlas/code/10-dp-1class-func/pytypes/classic_strategy.py
MD5-Checksum: a02fa3b98639f84a81b87d4f46007d51

本文件由 pytypes.typelogger v1.0b5 生成
生成时间 2020-05-02T15:50:59.987984.

类型信息基于运行时观察，运行环境为
CPython 3.8.2 final 0
/home/luciano/flupy/venv-3.8/bin/python3
    /home/luciano/flupy/venv-3.8/bin/pytest

警告：
如果你编辑了这个文件，请注意它是自动生成的。
请把你的自定义版本保存到其他位置；
本文件可能在不通知的情况下被覆盖。
"""

from classic_strategy import Customer, Promotion
from typing import Union



class LineItem(object):

    def __init__(self, product: str, quantity: int, price: float) -> None: ...
    def total(self) -> float: ...

class Order(object):

    def __init__(self, customer: Customer, cart: List[LineItem], promotion: Union[BulkItemPromo, FidelityPromo, LargeOrderPromo]) -> None: ...
    def total(self) -> float: ...
    def due(self) -> float: ...

class FidelityPromo(Promotion):

    def discount(self, order: Order) -> float: ...

class BulkItemPromo(Promotion):

    def discount(self, order: Order) -> float: ...

class LargeOrderPromo(Promotion):

    def discount(self, order: Order) -> float: ...
