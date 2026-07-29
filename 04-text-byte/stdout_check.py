import sys
from unicodedata import name

print(sys.version)
print()
print('sys.stdout.isatty():', sys.stdout.isatty())
print('sys.stdout.encoding:', sys.stdout.encoding)
print()

test_chars = [
    '\N{HORIZONTAL ELLIPSIS}',       # cp1252 中有，cp437 中没有
    '\N{INFINITY}',                  # cp437 中有，cp1252 中没有
    '\N{CIRCLED NUMBER FORTY TWO}',  # cp437 和 cp1252 中都没有
]

for char in test_chars:
    print(f'Trying to output {name(char)}:')
    print(char)
