"""
简短示例
===========

``UpperDict`` 的行为类似一个不区分大小写的映射（mapping）::

# tag::UPPERDICT_DEMO[]
    >>> d = UpperDict([('a', 'letter A'), (2, 'digit two')])
    >>> list(d.keys())
    ['A', 2]
    >>> d['b'] = 'letter B'
    >>> 'b' in d
    True
    >>> d['a'], d.get('B')
    ('letter A', 'letter B')
    >>> list(d.keys())
    ['A', 2, 'B']

# end::UPPERDICT_DEMO[]

而 ``UpperCounter`` 也不区分大小写::

# tag::UPPERCOUNTER_DEMO[]
    >>> c = UpperCounter('BaNanA')
    >>> c.most_common()
    [('A', 3), ('N', 2), ('B', 1)]

# end::UPPERCOUNTER_DEMO[]

详细测试
==============

UpperDict 将所有字符串键转换为大写。

    >>> d = UpperDict([('a', 'letter A'), ('B', 'letter B'), (2, 'digit two')])


使用 `d[key]` 表示法获取元素的测试::

    >>> d['A']
    'letter A'
    >>> d['b']
    'letter B'
    >>> d[2]
    'digit two'


缺失键的测试::

    >>> d['z']
    Traceback (most recent call last):
      ...
    KeyError: 'Z'
    >>> d[99]
    Traceback (most recent call last):
      ...
    KeyError: 99


使用 `d.get(key)` 表示法获取元素的测试::

    >>> d.get('a')
    'letter A'
    >>> d.get('B')
    'letter B'
    >>> d.get(2)
    'digit two'
    >>> d.get('z', '(not found)')
    '(not found)'

`in` 运算符的测试::

    >>> ('a' in d, 'B' in d, 'z' in d)
    (True, True, False)

使用小写键赋值元素的测试::

    >>> d['c'] = 'letter C'
    >>> d['C']
    'letter C'

使用 `dict` 或键值对序列进行 update 的测试::

    >>> d.update({'D': 'letter D', 'e': 'letter E'})
    >>> list(d.keys())
    ['A', 'B', 2, 'C', 'D', 'E']
    >>> d.update([('f', 'letter F'), ('G', 'letter G')])
    >>> list(d.keys())
    ['A', 'B', 2, 'C', 'D', 'E', 'F', 'G']
    >>> d  # doctest:+NORMALIZE_WHITESPACE
    {'A': 'letter A', 'B': 'letter B', 2: 'digit two',
    'C': 'letter C', 'D': 'letter D', 'E': 'letter E',
    'F': 'letter F', 'G': 'letter G'}

UpperCounter 将所有 `str` 键转换为大写。

初始化器测试：键被转换为大写。

    >>> d = UpperCounter('AbracAdaBrA')
    >>> sorted(d.keys())
    ['A', 'B', 'C', 'D', 'R']

使用 `d[key]` 表示法获取计数的测试::

    >>> d['a']
    5
    >>> d['z']
    0

"""
# tag::UPPERCASE_MIXIN[]
import collections

def _upper(key):  # <1>
    try:
        return key.upper()
    except AttributeError:
        return key

class UpperCaseMixin:  # <2>
    def __setitem__(self, key, item):
        super().__setitem__(_upper(key), item)

    def __getitem__(self, key):
        return super().__getitem__(_upper(key))

    def get(self, key, default=None):
        return super().get(_upper(key), default)

    def __contains__(self, key):
        return super().__contains__(_upper(key))
# end::UPPERCASE_MIXIN[]

# tag::UPPERDICT[]
class UpperDict(UpperCaseMixin, collections.UserDict):  # <1>
    pass

class UpperCounter(UpperCaseMixin, collections.Counter):  # <2>
    """专用的 'Counter'，会将字符串键转换为大写"""  # <3>
# end::UPPERDICT[]
