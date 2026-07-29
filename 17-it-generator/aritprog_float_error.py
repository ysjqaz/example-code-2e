"""
演示两种等差数列计算方式的差异：
一种通过反复累加增量（会累积误差），
另一种通过一次加法和一次乘法计算。
"""

from fractions import Fraction
from aritprog_v0 import ArithmeticProgression as APv0
from aritprog_v1 import ArithmeticProgression as APv1

if __name__ == '__main__':

    ap0 = iter(APv0(1, .1))
    ap1 = iter(APv1(1, .1))
    ap_frac = iter(APv1(Fraction(1, 1), Fraction(1, 10)))
    epsilon = 10**-10
    iteration = 0
    delta = next(ap0) - next(ap1)
    frac = next(ap_frac)
    while abs(delta) <= epsilon:
        delta = next(ap0) - next(ap1)
        frac = next(ap_frac)
        iteration += 1

    print('iteration: {}\tfraction: {}\tepsilon: {}\tdelta: {}'.
          format(iteration, frac, epsilon, delta))
