"""
unrelated.py：在兄弟类（sibling class）中使用 ``super()`` 的示例。

``U`` 是无关的（不是 ``Root`` 的子类）

对 ``U`` 的实例调用 ``ping`` 会失败::

# tag::UNRELATED_DEMO_1[]
    >>> u = U()
    >>> u.ping()
    Traceback (most recent call last):
      ...
    AttributeError: 'super' object has no attribute 'ping'

# end::UNRELATED_DEMO_1[]


但如果 ``U`` 是基类的协作安排（cooperative arrangement）的一部分，
其 ``ping`` 方法就能正常工作::

# tag::UNRELATED_DEMO_2[]

    >>> leaf2 = LeafUA()
    >>> leaf2.ping()
    <instance of LeafUA>.ping() in LeafUA
    <instance of LeafUA>.ping() in U
    <instance of LeafUA>.ping() in A
    <instance of LeafUA>.ping() in Root
    >>> LeafUA.__mro__  # doctest:+NORMALIZE_WHITESPACE
    (<class 'diamond2.LeafUA'>, <class 'diamond2.U'>,
     <class 'diamond.A'>, <class 'diamond.Root'>, <class 'object'>)

# end::UNRELATED_DEMO_2[]


这里 ``U.ping`` 永远不会被调用，因为 ``Root.ping`` 不调用 ``super``。

    >>> o6 = LeafAU()
    >>> o6.ping()
    <instance of LeafAU>.ping() in LeafAU
    <instance of LeafAU>.ping() in A
    <instance of LeafAU>.ping() in Root
    >>> LeafAU.__mro__  # doctest:+NORMALIZE_WHITESPACE
    (<class 'diamond2.LeafAU'>, <class 'diamond.A'>, <class 'diamond.Root'>,
     <class 'diamond2.U'>, <class 'object'>)

"""

# tag::DIAMOND_CLASSES[]
from diamond import A  # <1>

class U():  # <2>
    def ping(self):
        print(f'{self}.ping() in U')
        super().ping()  # <3>

class LeafUA(U, A):  # <4>
    def ping(self):
        print(f'{self}.ping() in LeafUA')
        super().ping()
# end::DIAMOND_CLASSES[]

class LeafAU(A, U):
    def ping(self):
        print(f'{self}.ping() in LeafAU')
        super().ping()

