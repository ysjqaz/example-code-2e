import pytest

from bunch import Bunch

class Point(Bunch):
    """ 一个点有 x、y 坐标（默认 0.0）和颜色（默认 'gray'）——
        除此之外什么也没有，只有 Python 和元类（metaclass）暗中加上的东西，
        比如 __init__ 和 __repr__
    """
    x = 0.0
    y = 0.0
    color = 'gray'


def test_init_defaults():
    p = Point()
    assert repr(p) == 'Point()'


def test_init():
    p = Point(x=1.2, y=3.4, color='red')
    assert repr(p) == "Point(x=1.2, y=3.4, color='red')"


def test_init_wrong_argument():
    with pytest.raises(AttributeError) as exc:
        p = Point(x=1.2, y=3.4, flavor='coffee')
    assert "no attribute 'flavor'" in str(exc.value)


def test_slots():
    p = Point()
    with pytest.raises(AttributeError) as exc:
        p.z = 5.6
    assert "no attribute 'z'" in str(exc.value)


