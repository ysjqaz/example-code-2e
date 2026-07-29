"""
Sentence：使用迭代器模式（Iterator Pattern）逐词迭代，第 2 版

警告：在惯用 Python 中，迭代器模式要简单得多；
参见 sentence_gen*.py。
"""

import re
import reprlib

RE_WORD = re.compile(r'\w+')


class Sentence:

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f'Sentence({reprlib.repr(self.text)})'

    def __iter__(self):
        word_iter = RE_WORD.finditer(self.text)  # <1>
        return SentenceIter(word_iter)  # <2>


class SentenceIter:

    def __init__(self, word_iter):
        self.word_iter = word_iter  # <3>

    def __next__(self):
        match = next(self.word_iter)  # <4>
        return match.group()  # <5>

    def __iter__(self):
        return self
