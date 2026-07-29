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

该上下文管理器可以处理并「吞掉」异常。
下面的测试在 doctest 下无法通过（doctest 会报告
ZeroDivisionError），但在 Python 3 控制台中
手工执行则能通过（异常由上下文管理器处理）：

# tag::MIRROR_GEN_DEMO_3[]

    >>> from mirror_gen_exc import looking_glass
    >>> with looking_glass():
    ...      print('Humpty Dumpty')
    ...      x = 1/0  # <1>
    ...      print('END')  # <2>
    ...
    ytpmuD ytpmuH
    Please DO NOT divide by zero!

# end::MIRROR_GEN_DEMO_3[]

    >>> with looking_glass():
    ...      print('Humpty Dumpty')
    ...      x = no_such_name  # <1>
    ...      print('END')  # <2>
    ...
    Traceback (most recent call last):
      ...
    NameError: name 'no_such_name' is not defined



"""


# tag::MIRROR_GEN_EXC[]
import contextlib
import sys

@contextlib.contextmanager
def looking_glass():
    original_write = sys.stdout.write

    def reverse_write(text):
        original_write(text[::-1])

    sys.stdout.write = reverse_write
    msg = ''  # <1>
    try:
        yield 'JABBERWOCKY'
    except ZeroDivisionError:  # <2>
        msg = 'Please DO NOT divide by zero!'
    finally:
        sys.stdout.write = original_write  # <3>
        if msg:
            print(msg)  # <4>
# end::MIRROR_GEN_EXC[]
