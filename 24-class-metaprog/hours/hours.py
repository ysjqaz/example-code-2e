"""
滥用 ``__class_getitem__`` 来造一个处理小时、分钟、秒（后两者按 60 进制）的微型 DSL。

``H`` 是 ``Hours`` 类的别名::

    >>> H[1]
    1:00
    >>> H[1:30]
    1:30
    >>> H[1::5]
    1:00:05
    >>> H[::5]
    0:00:05

``H`` 实例可以转换为以小时为单位的浮点数::

    >>> float(H[1:15])
    1.25
    >>> float(H[1:30:30])  # doctest: +ELLIPSIS
    1.5083333...
    >>> float(H[1::5])     # doctest: +ELLIPSIS
    1.0013888...

``H`` 构造器接受小时、分钟和/或秒::

    >>> H(1.5)
    1:30
    >>> H(1.9)
    1:54
    >>> H(1, 30, 30)
    1:30:30
    >>> H(s = 7205)
    2:00:05
    >>> H(1/3)
    0:20
    >>> H(1/1000)
    0:00:03.6

``H`` 实例是可迭代对象（iterable），便于解包::

    >>> hms = H[1:22:33]
    >>> h, m, s = hms
    >>> h, m, s
    (1, 22, 33)
    >>> tuple(hms)
    (1, 22, 33)


``H`` 实例可以相加::

    >>> H[1:45:12] + H[2:15:50]
    4:01:02
"""

from typing import Tuple, Union


def normalize(s: float) -> Tuple[int, int, float]:
    h, r = divmod(s, 3600)
    m, s = divmod(r, 60)
    return int(h), int(m), s


def valid_base_60(n, unit):
    if not (0 <= n < 60):
        raise ValueError(f'invalid {unit} {n}')
    return n


class Hours:
    h: int
    _m: int
    _s: float

    def __class_getitem__(cls, parts: Union[slice, float]) -> 'Hours':
        if isinstance(parts, slice):
            h = parts.start or 0
            m = valid_base_60(parts.stop or 0, 'minutes')
            s = valid_base_60(parts.step or 0, 'seconds')
        else:
            h, m, s = normalize(parts * 3600)
        return Hours(h, m, s)

    def __init__(self, h: float = 0, m: float = 0, s: float = 0):
        if h < 0 or m < 0 or s < 0:
            raise ValueError('invalid negative argument')
        self.h, self.m, self.s = normalize(h * 3600 + m * 60 + s)

    def __repr__(self):
        h, m, s = self
        display_s = f'{s:06.3f}'
        display_s = display_s.rstrip('0').rstrip('.')
        if display_s == '00':
            return f'{h}:{m:02d}'
        return f'{h}:{m:02d}:{display_s}'

    def __float__(self):
        return self.h + self.m / 60 + self.s / 3600

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __iter__(self):
        yield self.h
        yield self.m
        yield self.s

    def __add__(self, other):
        if not isinstance(other, Hours):
            return NotImplemented
        return Hours(*(a + b for a, b in zip(self, other)))


H = Hours
