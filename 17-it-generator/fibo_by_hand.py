"""
「手工」实现的斐波那契生成器（generator），不使用生成器对象

    >>> from itertools import islice
    >>> list(islice(Fibonacci(), 15))
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]

"""


# tag::FIBO_BY_HAND[]
class Fibonacci:

    def __iter__(self):
        return FibonacciGenerator()


class FibonacciGenerator:

    def __init__(self):
        self.a = 0
        self.b = 1

    def __next__(self):
        result = self.a
        self.a, self.b = self.b, self.a + self.b
        return result

    def __iter__(self):
        return self
# end::FIBO_BY_HAND[]

# 作为对比，下面是 Python 中常见的斐波那契生成器实现：


def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


if __name__ == '__main__':

    for x, y in zip(Fibonacci(), fibonacci()):
        assert x == y, f'{x} != {y}'
        print(x)
        if x > 10**10:
            break
    print('etc...')

