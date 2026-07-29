"""
``name_index`` 构建一个倒排索引（inverted index），将单词映射到名称中包含该单词的
Unicode 字符集合。例如::

    >>> index = name_index(32, 65)
    >>> sorted(index['SIGN'])
    ['#', '$', '%', '+', '<', '=', '>']
    >>> sorted(index['DIGIT'])
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    >>> index['DIGIT'] & index['EIGHT']
    {'8'}
"""

# tag::CHARINDEX[]
import sys
import re
import unicodedata
from collections.abc import Iterator

RE_WORD = re.compile(r'\w+')
STOP_CODE = sys.maxunicode + 1

def tokenize(text: str) -> Iterator[str]:  # <1>
    """返回大写单词的可迭代对象"""
    for match in RE_WORD.finditer(text):
        yield match.group().upper()

def name_index(start: int = 32, end: int = STOP_CODE) -> dict[str, set[str]]:
    index: dict[str, set[str]] = {}  # <2>
    for char in (chr(i) for i in range(start, end)):
        if name := unicodedata.name(char, ''):  # <3>
            for word in tokenize(name):
                index.setdefault(word, set()).add(char)
    return index
# end::CHARINDEX[]
