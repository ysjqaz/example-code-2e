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
    assert 'flavor' in str(exc.value)


def test_slots():
    p = Point()
    with pytest.raises(AttributeError) as exc:
        p.z = 5.6
    assert "no attribute 'z'" in str(exc.value)


def test_dunder_permitted():
    class Cat(Bunch):
        name = ''
        weight = 0

        def __str__(self):
            return f'{self.name} ({self.weight} kg)'

    cheshire = Cat(name='Cheshire')
    assert str(cheshire) == 'Cheshire (0 kg)'


def test_dunder_forbidden():
    with pytest.raises(AttributeError) as exc:
        class Cat(Bunch):
            name = ''
            weight = 0

            def __init__(self):
                pass
    assert "Can't set '__init__' in 'Cat'" in str(exc.value)
