"""
``tombola.Tombola`` 的一个变体，实现了 ``__subclasshook__``。

用简单类做测试::

    >>> Tombola.__subclasshook__(object)
    NotImplemented
    >>> class Complete:
    ...     def __init__(): pass
    ...     def load(): pass
    ...     def pick(): pass
    ...     def loaded(): pass
    ...
    >>> Tombola.__subclasshook__(Complete)
    True
    >>> issubclass(Complete, Tombola)

"""


from abc import ABC, abstractmethod
from inspect import getmembers, isfunction


class Tombola(ABC):  # <1>

    @abstractmethod
    def __init__(self, iterable):  # <2>
        """新实例从一个可迭代对象加载而来。"""

    @abstractmethod
    def load(self, iterable):
        """从一个可迭代对象中加载元素。"""

    @abstractmethod
    def pick(self):  # <3>
        """随机移除一个元素并返回它。

        当实例为空时，本方法应抛出 `LookupError`。
        """

    def loaded(self):  # <4>
        try:
            item = self.pick()
        except LookupError:
            return False
        else:
            self.load([item])  # 把它放回去
            return True

    @classmethod
    def __subclasshook__(cls, other_cls):
        if cls is Tombola:
            interface_names = function_names(cls)
            found_names = set()
            for a_cls in other_cls.__mro__:
                found_names |= function_names(a_cls)
            if found_names >= interface_names:
                return True
        return NotImplemented


def function_names(obj):
    return {name for name, _ in getmembers(obj, isfunction)}
