"""
在 ``Generator[YieldType, SendType, ReturnType]`` 中，
``SendType`` 是逆变（contravariant）的。
其他类型变量是协变（covariant）的。

``typing.Generator`` 的声明如下::

    class Generator(Iterator[T_co], Generic[T_co, T_contra, V_co]):

（来自 https://docs.python.org/3/library/typing.html#typing.Generator）

"""

from typing import Generator


# Generator[YieldType, SendType, ReturnType]

def gen_float_take_int() -> Generator[float, int, str]:
    received = yield -1.0
    while received:
        received = yield float(received)
    return 'Done'


def gen_float_take_float() -> Generator[float, float, str]:
    received = yield -1.0
    while received:
        received = yield float(received)
    return 'Done'


def gen_float_take_complex() -> Generator[float, complex, str]:
    received = yield -1.0
    while received:
        received = yield abs(received)
    return 'Done'

# Generator[YieldType, SendType, ReturnType]

g0: Generator[float, float, str] = gen_float_take_float()

g1: Generator[complex, float, str] = gen_float_take_float()

## 赋值时类型不兼容
##   表达式类型为 "Generator[float, float, str]"
##     变量类型为 "Generator[int, float, str]")
# g2: Generator[int, float, str] = gen_float_take_float()


# Generator[YieldType, SendType, ReturnType]

g3: Generator[float, int, str] = gen_float_take_float()

## 赋值时类型不兼容
##   表达式类型为 "Generator[float, float, str]"
##     变量类型为 "Generator[float, complex, str]")
## g4: Generator[float, complex, str] = gen_float_take_float()

