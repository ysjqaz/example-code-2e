"""
一个「镜像」``stdout`` 的上下文管理器（context manager）。

当处于活动状态时，该上下文管理器会将写入 ``stdout`` 的
文本反转输出::

# tag::MIRROR_GEN_DEMO_1[]

    >>> from mirror_gen import looking_glass
    >>> with looking_glass() as what:  # <1>
    ...      print('Alice, Kitty and Snowdrop')
    ...      print(what)
    ...
    pordwonS dna yttiK ,ecilA
    YKCOWREBBAJ
    >>> what
    'JABBERWOCKY'
    >>> print('back to normal')
    back to normal


# end::MIRROR_GEN_DEMO_1[]


下面展示了上下文管理器的内部运作::

# tag::MIRROR_GEN_DEMO_2[]

    >>> from mirror_gen import looking_glass
    >>> manager = looking_glass()  # <1>
    >>> manager  # doctest: +ELLIPSIS
    <contextlib._GeneratorContextManager object at 0x...>
    >>> monster = manager.__enter__()  # <2>
    >>> monster == 'JABBERWOCKY'  # <3>
    eurT
    >>> monster
    'YKCOWREBBAJ'
    >>> manager  # doctest: +ELLIPSIS
    >...x0 ta tcejbo reganaMtxetnoCrotareneG_.biltxetnoc<
    >>> manager.__exit__(None, None, None)  # <4>
    False
    >>> monster
    'JABBERWOCKY'

# end::MIRROR_GEN_DEMO_2[]

被装饰的生成器（generator）还可以作为装饰器使用：


# tag::MIRROR_GEN_DECO[]
    >>> @looking_glass()
    ... def verse():
    ...     print('The time has come')
    ...
    >>> verse()  # <1>
    emoc sah emit ehT
    >>> print('back to normal')  # <2>
    back to normal

# end::MIRROR_GEN_DECO[]

"""


# tag::MIRROR_GEN_EX[]
import contextlib
import sys

@contextlib.contextmanager  # <1>
def looking_glass():
    original_write = sys.stdout.write  # <2>

    def reverse_write(text):  # <3>
        original_write(text[::-1])

    sys.stdout.write = reverse_write  # <4>
    yield 'JABBERWOCKY'  # <5>
    sys.stdout.write = original_write  # <6>
# end::MIRROR_GEN_EX[]
