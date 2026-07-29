domainlib demonstration
=======================

domainlib 演示
==============

运行 Python 的 async 控制台（需要 Python ≥ 3.8）::

    $ python3 -m asyncio

会看到 ``asyncio`` 已被自动导入::

    >>> import asyncio

现在可以开始实验 ``domainlib`` 了。

在 ``>>>`` 提示符下，输入以下命令::

    >>> from domainlib import *
    >>> await probe('python.org')

注意观察结果。

接着::

    >>> names = 'python.org rust-lang.org golang.org n05uch1an9.org'.split()
    >>> async for result in multi_probe(names):
    ...     print(*result, sep='\t')

注意：如果再次运行最后两行，
结果出现的顺序很可能不同。
