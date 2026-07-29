"""Transformdict：在查找时转换键的映射

本模块和 ``test_transformdict.py`` 提取自 Antoine Pitrou 向 Python 贡献的一个补丁，该补丁实现了他的 PEP 455——向 collections 添加一个键转换字典。该 PEP 被拒绝，补丁也从未合并到 CPython。原始代码在 ``transformdict3.patch`` 中，属于 issue #18986：添加一个不区分大小写但保留大小写的字典。

http://bugs.python.org/issue18986
"""

from collections.abc import MutableMapping


_sentinel = object()


class TransformDict(MutableMapping):
    """在查找键时调用转换函数、但保留原始键的字典。

    >>> d = TransformDict(str.lower)
    >>> d['Foo'] = 5
    >>> d['foo'] == d['FOO'] == d['Foo'] == 5
    True
    >>> set(d.keys())
    {'Foo'}
    """

    __slots__ = ('_transform', '_original', '_data')

    def __init__(self, transform, init_dict=None, **kwargs):
        """用给定的 *transform* 函数创建一个新的 TransformDict。
        *init_dict* 和 *kwargs* 是可选的初始化器，用法与 dict 构造器相同。
        """
        if not callable(transform):
            raise TypeError(
                f'expected a callable, got {transform.__class__!r}')
        self._transform = transform
        # 转换后的键 => 原始键
        self._original = {}
        self._data = {}
        if init_dict:
            self.update(init_dict)
        if kwargs:
            self.update(kwargs)

    def getitem(self, key):
        """D.getitem(key) -> (存储的键, 值)"""
        transformed = self._transform(key)
        original = self._original[transformed]
        value = self._data[transformed]
        return original, value

    @property
    def transform_func(self):
        """这是 TransformDict 的转换函数"""
        return self._transform

    # MutableMapping 要求的最小方法集

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._original.values())

    def __getitem__(self, key):
        return self._data[self._transform(key)]

    def __setitem__(self, key, value):
        transformed = self._transform(key)
        self._data[transformed] = value
        self._original.setdefault(transformed, key)

    def __delitem__(self, key):
        transformed = self._transform(key)
        del self._data[transformed]
        del self._original[transformed]

    # 为减轻性能开销而覆盖的方法。

    def clear(self):
        """D.clear() -> None.  移除 D 中的所有元素。"""
        self._data.clear()
        self._original.clear()

    def __contains__(self, key):
        return self._transform(key) in self._data

    def get(self, key, default=None):
        """D.get(k[,d]) -> 如果 k 在 D 中则返回 D[k]，否则返回 d。d 默认为 None。"""
        return self._data.get(self._transform(key), default)

    def pop(self, key, default=_sentinel):
        """D.pop(k[,d]) -> v，移除键并返回对应的值。
           如果找不到键，则返回 d（如果给定），否则
           抛出 KeyError。
        """
        transformed = self._transform(key)
        if default is _sentinel:
            del self._original[transformed]
            return self._data.pop(transformed)
        else:
            self._original.pop(transformed, None)
            return self._data.pop(transformed, default)

    def popitem(self):
        """D.popitem() -> (k, v)，移除并返回某个 (键, 值) 对
           作为二元组；但如果 D 为空则抛出 KeyError。
        """
        transformed, value = self._data.popitem()
        return self._original.pop(transformed), value

    # 其他方法

    def copy(self):
        """D.copy() -> D 的浅拷贝"""
        other = self.__class__(self._transform)
        other._original = self._original.copy()
        other._data = self._data.copy()
        return other

    __copy__ = copy

    def __getstate__(self):
        return (self._transform, self._data, self._original)

    def __setstate__(self, state):
        self._transform, self._data, self._original = state

    def __repr__(self):
        try:
            equiv = dict(self)
        except TypeError:
            # 某些键不可哈希，回退到 .items()
            equiv = list(self.items())
        return f'{self.__class__.__name__}({self._transform!r}, {equiv!r})'
