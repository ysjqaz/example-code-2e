"""
``__missing__`` 在各种映射（mapping）中的语义。

✅ = 表示调用了 ``__missing__``

``dict`` 的子类::

    >>> d = DictSub(A = 'letter A')
    >>> d['a']  # ✅
    'letter A'
    >>> d.get('a', '')
    ''
    >>> 'a' in d
    False

``UserDict`` 的子类::

    >>> ud = UserDictSub(A = 'letter A')
    >>> ud['a']  # ✅
    'letter A'
    >>> ud.get('a', '')  # ✅
    'letter A'
    >>> 'a' in ud
    False


``abc.Mapping`` 的简单子类::

    >>> sms = SimpleMappingSub(A = 'letter A')
    >>> sms['a']
    Traceback (most recent call last):
      ...
    KeyError: 'a'
    >>> sms.get('a', '')
    ''
    >>> 'a' in sms
    False


支持 ``__missing__`` 的 ``abc.Mapping`` 子类::

    >>> mms = MappingMissingSub(A = 'letter A')
    >>> mms['a']  # ✅
    'letter A'
    >>> mms.get('a', '')  # ✅
    'letter A'
    >>> 'a' in mms  # ✅
    True

支持 ``__missing__`` 的 ``abc.Mapping`` 子类::

    >>> dms = DictLikeMappingSub(A = 'letter A')
    >>> dms['a']  # ✅
    'letter A'
    >>> dms.get('a', '')
    ''
    >>> 'a' in dms
    False


"""

from collections import UserDict
from collections import abc


def _upper(x):
    try:
        return x.upper()
    except AttributeError:
        return x


class DictSub(dict):
    def __missing__(self, key):
        return self[_upper(key)]


class UserDictSub(UserDict):
    def __missing__(self, key):
        return self[_upper(key)]


class SimpleMappingSub(abc.Mapping):
    def __init__(self, *args, **kwargs):
        self._data = dict(*args, **kwargs)

    # 接下来三个方法：在 ABC 中是抽象方法
    def __getitem__(self, key):
        return self._data[key]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    # 永远不会被此类的实例调用
    def __missing__(self, key):
        return self[_upper(key)]


class MappingMissingSub(SimpleMappingSub):
    def __getitem__(self, key):
        try:
            return self._data[key]
        except KeyError:
            return self[_upper(key)]


class DictLikeMappingSub(SimpleMappingSub):
    def __getitem__(self, key):
        try:
            return self._data[key]
        except KeyError:
            return self[_upper(key)]

    def get(self, key, default=None):
        return self._data.get(key, default)

    def __contains__(self, key):
        return key in self._data
