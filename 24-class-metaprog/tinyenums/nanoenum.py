# 这是 João S. O. Bueno (@gwidion) 一个想法的简化版，
# 他私下分享给我，并允许在《Fluent Python 2e》中使用。

"""
测试 ``KeyIsValueDict``::

    >>> adict = KeyIsValueDict()
    >>> len(adict)
    0
    >>> adict['first']
    'first'
    >>> adict
    {'first': 'first'}
    >>> adict['second']
    'second'
    >>> len(adict)
    2
    >>> adict
    {'first': 'first', 'second': 'second'}
    >>> adict['__magic__']
    Traceback (most recent call last):
      ...
    KeyError: '__magic__'
"""


class KeyIsValueDict(dict):
    def __missing__(self, key):
        if key.startswith('__') and key.endswith('__'):
            raise KeyError(key)
        self[key] = key
        return key


class NanoEnumMeta(type):
    def __prepare__(name, bases, **kwargs):
        return KeyIsValueDict()


class NanoEnum(metaclass=NanoEnumMeta):
    pass
