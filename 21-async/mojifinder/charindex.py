#!/usr/bin/env python

"""
``InvertedIndex`` 类构建一个倒排索引（inverted index），将每个单词
映射到名字中包含该单词的 Unicode 字符集合。

构造函数的可选参数 ``first`` 和 ``last+1`` 是要建立索引的字符代码
起止位置，这是为了方便测试。在下面的示例中，只对 ASCII 范围建立了索引。

`entries` 属性是一个 `defaultdict`，以大写的单个单词作为键::

    >>> idx = InvertedIndex(32, 128)
    >>> idx.entries['DOLLAR']
    {'$'}
    >>> sorted(idx.entries['SIGN'])
    ['#', '$', '%', '+', '<', '=', '>']
    >>> idx.entries['A'] & idx.entries['SMALL']
    {'a'}
    >>> idx.entries['BRILLIG']
    set()

`.search()` 方法接收一个字符串，将其大写、拆分为单词，
并返回各单词对应条目的交集::

    >>> idx.search('capital a')
    {'A'}

"""

import sys
import unicodedata
from collections import defaultdict
from collections.abc import Iterator

STOP_CODE: int = sys.maxunicode + 1

Char = str
Index = defaultdict[str, set[Char]]


def tokenize(text: str) -> Iterator[str]:
    """返回大写单词的迭代器"""
    for word in text.upper().replace('-', ' ').split():
        yield word


class InvertedIndex:
    entries: Index

    def __init__(self, start: int = 32, stop: int = STOP_CODE):
        entries: Index = defaultdict(set)
        for char in (chr(i) for i in range(start, stop)):
            name = unicodedata.name(char, '')
            if name:
                for word in tokenize(name):
                    entries[word].add(char)
        self.entries = entries

    def search(self, query: str) -> set[Char]:
        if words := list(tokenize(query)):
            found = self.entries[words[0]]
            return found.intersection(*(self.entries[w] for w in words[1:]))
        else:
            return set()


def format_results(chars: set[Char]) -> Iterator[str]:
    for char in sorted(chars):
        name = unicodedata.name(char)
        code = ord(char)
        yield f'U+{code:04X}\t{char}\t{name}'


def main(words: list[str]) -> None:
    if not words:
        print('Please give one or more words to search.')
        sys.exit(2)  # 命令行用法错误
    index = InvertedIndex()
    chars = index.search(' '.join(words))
    for line in format_results(chars):
        print(line)
    print('─' * 66, f'{len(chars)} found')


if __name__ == '__main__':
    main(sys.argv[1:])
