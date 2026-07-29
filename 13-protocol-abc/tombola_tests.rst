==============
Tombola 测试
==============

Tombola 的每个具体子类都应通过这些测试。


从可迭代对象创建并加载实例::

    >>> balls = list(range(3))
    >>> globe = ConcreteTombola(balls)
    >>> globe.loaded()
    True
    >>> sorted(globe.inspect())
    [0, 1, 2]


抽取并收集球::

    >>> picks = []
    >>> picks.append(globe.pick())
    >>> picks.append(globe.pick())
    >>> picks.append(globe.pick())


检查状态和结果::

    >>> globe.loaded()
    False
    >>> sorted(picks) == balls
    True


重新加载::

    >>> globe.load(balls)
    >>> globe.loaded()
    True
    >>> picks = [globe.pick() for i in balls]
    >>> globe.loaded()
    False


检查当设备为空时抛出的是 `LookupError`（或其子类）异常::

    >>> globe = ConcreteTombola([])
    >>> try:
    ...     globe.pick()
    ... except LookupError as exc:
    ...     print('OK')
    OK


加载并抽取 100 个球，验证它们全部被抽出::

    >>> balls = list(range(100))
    >>> globe = ConcreteTombola(balls)
    >>> picks = []
    >>> while globe.inspect():
    ...     picks.append(globe.pick())
    >>> len(picks) == len(balls)
    True
    >>> set(picks) == set(balls)
    True


检查顺序已改变，而非简单反转::

    >>> picks != balls
    True
    >>> picks[::-1] != balls
    True

注：即使实现正确，上面 2 个测试也有*极小*的概率失败。100 个球
恰好按 inspect 时的顺序被抽出的概率是 1/100!，约为
1.07e-158。这比中彩票或者靠写程序成为亿万富翁还要容易得多。

全文完

