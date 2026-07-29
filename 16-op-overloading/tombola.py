# BEGIN TOMBOLA_ABC

import abc

class Tombola(abc.ABC):  # <1>

    @abc.abstractmethod
    def load(self, iterable):  # <2>
        """从可迭代对象（iterable）中加载元素。"""

    @abc.abstractmethod
    def pick(self):  # <3>
        """随机移除一个元素并返回它。

        当实例为空时，本方法应抛出 `LookupError`。
        """

    def loaded(self):  # <4>
        """如果至少有 1 个元素则返回 `True`，否则返回 `False`。"""
        return bool(self.inspect())  # <5>

    def inspect(self):
        """返回一个按排序后的元组，包含当前内部的所有元素。"""
        items = []
        while True:  # <6>
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)  # <7>
        return tuple(sorted(items))

# END TOMBOLA_ABC

