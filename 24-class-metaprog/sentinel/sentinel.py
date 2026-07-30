"""
本模块提供一个 ``Sentinel`` 类，可以直接作为哨兵单例使用，
也可以子类化以获得一个独立的哨兵单例。

``Sentinel`` 类的 ``repr`` 是它的名字::

    >>> class Missing(Sentinel): pass
    >>> Missing
    Missing

如果需要不同的 ``repr``，
可以把它定义为类属性（attribute）::

    >>> class CustomRepr(Sentinel):
    ...     repr = '<CustomRepr>'
    ...
    >>> CustomRepr
    <CustomRepr>

``Sentinel`` 类不能被实例化::

    >>> Missing()
    Traceback (most recent call last):
      ...
    TypeError: 'Missing' is a sentinel and cannot be instantiated

"""


class _SentinelMeta(type):
    def __repr__(cls):
        try:
            return cls.repr
        except AttributeError:
            return cls.__name__


class Sentinel(metaclass=_SentinelMeta):
    def __new__(cls):
        msg = 'is a sentinel and cannot be instantiated'
        raise TypeError(f"'{cls!r}' {msg}")
