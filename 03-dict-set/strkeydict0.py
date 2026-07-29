"""StrKeyDict0 在查找时将非字符串键转换为 `str`

# tag::STRKEYDICT0_TESTS[]

使用 `d[key]` 表示法获取元素的测试::

    >>> d = StrKeyDict0([('2', 'two'), ('4', 'four')])
    >>> d['2']
    'two'
    >>> d[4]
    'four'
    >>> d[1]
    Traceback (most recent call last):
      ...
    KeyError: '1'

使用 `d.get(key)` 表示法获取元素的测试::

    >>> d.get('2')
    'two'
    >>> d.get(4)
    'four'
    >>> d.get(1, 'N/A')
    'N/A'


`in` 运算符的测试::

    >>> 2 in d
    True
    >>> 1 in d
    False

# end::STRKEYDICT0_TESTS[]
"""


# tag::STRKEYDICT0[]
class StrKeyDict0(dict):  # <1>

    def __missing__(self, key):
        if isinstance(key, str):  # <2>
            raise KeyError(key)
        return self[str(key)]  # <3>

    def get(self, key, default=None):
        try:
            return self[key]  # <4>
        except KeyError:
            return default  # <5>

    def __contains__(self, key):
        return key in self.keys() or str(key) in self.keys()  # <6>

# end::STRKEYDICT0[]
