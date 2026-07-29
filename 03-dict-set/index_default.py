# 改编自 Alex Martelli 在「Re-learning Python」中的示例
# http://www.aleax.it/Python/accu04_Relearn_Python_alex.pdf
# （第 41 页）练习：按单词建文件索引

# tag::INDEX_DEFAULT[]
"""构建一个索引：单词 -> 出现位置列表"""

import collections
import re
import sys

WORD_RE = re.compile(r'\w+')

index = collections.defaultdict(list)     # <1>
with open(sys.argv[1], encoding='utf-8') as fp:
    for line_no, line in enumerate(fp, 1):
        for match in WORD_RE.finditer(line):
            word = match.group()
            column_no = match.start() + 1
            location = (line_no, column_no)
            index[word].append(location)  # <2>

# 按字母顺序显示
for word in sorted(index, key=str.upper):
    print(word, index[word])
# end::INDEX_DEFAULT[]
