========================
Character Finder Utility
========================

字符查找工具（Character Finder Utility）

使用技巧
========

在类 Unix 系统上，如果 `$PATH` 中有 `python3`，
`cf.py` 可以作为可执行文件运行::

    $ chmod +x cf.py
    $ ./cf.py cat eyes
    U+1F638	😸	GRINNING CAT FACE WITH SMILING EYES
    U+1F63B	😻	SMILING CAT FACE WITH HEART-SHAPED EYES
    U+1F63D	😽	KISSING CAT FACE WITH CLOSED EYES

用 `wc -l` 统计命中数量::

    $ ./cf.py hieroglyph | wc -l
    1663

用 `tee` 可以同时得到输出和计数::

    $ ./cf.py trigram | tee >(wc -l)
    U+2630	☰	TRIGRAM FOR HEAVEN
    U+2631	☱	TRIGRAM FOR LAKE
    U+2632	☲	TRIGRAM FOR FIRE
    U+2633	☳	TRIGRAM FOR THUNDER
    U+2634	☴	TRIGRAM FOR WIND
    U+2635	☵	TRIGRAM FOR WATER
    U+2636	☶	TRIGRAM FOR MOUNTAIN
    U+2637	☷	TRIGRAM FOR EARTH
    8


运行测试
========

在命令行中对本 README.rst 文件运行 ``doctest`` 模块
（使用 ``-v`` 让测试过程可见）::

    $ python3 -m doctest README.rst -v

这正是 ``test.sh`` 脚本所做的事情。


测试
----

导入需要测试的函数::

    >>> from cf import find, main

测试 ``find`` 返回单个结果::

    >>> find('sign', 'registered')  # doctest:+NORMALIZE_WHITESPACE
    U+00AE	®	REGISTERED SIGN

测试 ``find`` 返回两个结果::

    >>> find('chess', 'queen', end=0xFFFF)  # doctest:+NORMALIZE_WHITESPACE
    U+2655	♕	WHITE CHESS QUEEN
    U+265B	♛	BLACK CHESS QUEEN

测试 ``find`` 无结果::

    >>> find('no_such_character')

测试 ``main`` 不传单词::

    >>> main([])
    Please provide words to find.
