# tag::TOMBOLA_ABC[]

import abc

class Tombola(abc.ABC):  # <1>

    @abc.abstractmethod
    def load(self, iterable):  # <2>
        """从一个可迭代对象中添加元素。"""

    @abc.abstractmethod
    def pick(self):  # <3>
        """随机移除一个元素并返回它。

        当实例为空时，此方法应当抛出 `LookupError`。
        """

    def loaded(self):  # <4>
        """如果至少有 1 个元素则返回 `True`，否则返回 `False`。"""
        return bool(self.inspect())  # <5>

    def inspect(self):
        """返回当前内部元素的已排序元组。"""
        items = []
        while True:  # <6>
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)  # <7>
        return tuple(items)


# end::TOMBOLA_ABC[]
