"""
Sentence：使用生成器函数逐词迭代
"""

# tag::SENTENCE_GEN[]
import re
import reprlib

RE_WORD = re.compile(r'\w+')


class Sentence:

    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        for word in self.words:  # <1>
            yield word  # <2>
        # <3>

# 完成！<4>

# end::SENTENCE_GEN[]
