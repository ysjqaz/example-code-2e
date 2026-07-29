==============================
``Sentence`` 类测试
==============================

``Sentence`` 由一个 ``str`` 构造，支持逐词迭代。

::
    >>> s = Sentence('The time has come')
    >>> s
    Sentence('The time has come')
    >>> list(s)
    ['The', 'time', 'has', 'come']
    >>> it = iter(s)
    >>> next(it)
    'The'
    >>> next(it)
    'time'
    >>> next(it)
    'has'
    >>> next(it)
    'come'
    >>> next(it)
    Traceback (most recent call last):
      ...
    StopIteration


迭代时会跳过任何标点符号::

    >>> s = Sentence('"The time has come," the Walrus said,')
    >>> s
    Sentence('"The time ha... Walrus said,')
    >>> list(s)
    ['The', 'time', 'has', 'come', 'the', 'Walrus', 'said']


包含换行符的空白字符也会被忽略::

    >>> s = Sentence('''"The time has come," the Walrus said,
    ...                 "To talk of many things:"''')
    >>> s
    Sentence('"The time ha...many things:"')
    >>> list(s)
    ['The', 'time', 'has', 'come', 'the', 'Walrus', 'said', 'To', 'talk', 'of', 'many', 'things']


带重音的拉丁字母也会被识别为单词字符::

    >>> s = Sentence('Agora vou-me. Ou me vão?')
    >>> s
    Sentence('Agora vou-me. Ou me vão?')
    >>> list(s)
    ['Agora', 'vou', 'me', 'Ou', 'me', 'vão']
