
"""
激进折叠与变音符号（diacritic mark）移除。

处理包含 `cp1252` 符号的字符串：

    >>> order = '“Herr Voß: • ½ cup of Œtker™ caffè latte • bowl of açaí.”'
    >>> shave_marks(order)
    '“Herr Voß: • ½ cup of Œtker™ caffe latte • bowl of acai.”'
    >>> shave_marks_latin(order)
    '“Herr Voß: • ½ cup of Œtker™ caffe latte • bowl of acai.”'
    >>> dewinize(order)
    '"Herr Voß: - ½ cup of OEtker(TM) caffè latte - bowl of açaí."'
    >>> asciize(order)
    '"Herr Voss: - 1⁄2 cup of OEtker(TM) caffe latte - bowl of acai."'

处理包含希腊语和拉丁语带重音字符的字符串：

    >>> greek = 'Ζέφυρος, Zéfiro'
    >>> shave_marks(greek)
    'Ζεφυρος, Zefiro'
    >>> shave_marks_latin(greek)
    'Ζέφυρος, Zefiro'
    >>> dewinize(greek)
    'Ζέφυρος, Zéfiro'
    >>> asciize(greek)
    'Ζέφυρος, Zefiro'

"""

# tag::SHAVE_MARKS[]
import unicodedata
import string


def shave_marks(txt):
    """移除所有变音符号"""
    norm_txt = unicodedata.normalize('NFD', txt)  # <1>
    shaved = ''.join(c for c in norm_txt
                     if not unicodedata.combining(c))  # <2>
    return unicodedata.normalize('NFC', shaved)  # <3>
# end::SHAVE_MARKS[]

# tag::SHAVE_MARKS_LATIN[]
def shave_marks_latin(txt):
    """移除拉丁语基础字符上的所有变音符号"""
    norm_txt = unicodedata.normalize('NFD', txt)  # <1>
    latin_base = False
    preserve = []
    for c in norm_txt:
        if unicodedata.combining(c) and latin_base:   # <2>
            continue  # 忽略拉丁语基础字符上的变音符号
        preserve.append(c)                            # <3>
        # 如果不是组合字符，那就是一个新的基础字符
        if not unicodedata.combining(c):              # <4>
            latin_base = c in string.ascii_letters
    shaved = ''.join(preserve)
    return unicodedata.normalize('NFC', shaved)   # <5>
# end::SHAVE_MARKS_LATIN[]

# tag::ASCIIZE[]
single_map = str.maketrans("""‚ƒ„ˆ‹‘’“”•–—˜›""",  # <1>
                           """'f"^<''""---~>""")

multi_map = str.maketrans({  # <2>
    '€': 'EUR',
    '…': '...',
    'Æ': 'AE',
    'æ': 'ae',
    'Œ': 'OE',
    'œ': 'oe',
    '™': '(TM)',
    '‰': '<per mille>',
    '†': '**',
    '‡': '***',
})

multi_map.update(single_map)  # <3>


def dewinize(txt):
    """将 Win1252 符号替换为 ASCII 字符或字符序列"""
    return txt.translate(multi_map)  # <4>


def asciize(txt):
    no_marks = shave_marks_latin(dewinize(txt))     # <5>
    no_marks = no_marks.replace('ß', 'ss')          # <6>
    return unicodedata.normalize('NFKC', no_marks)  # <7>
# end::ASCIIZE[]
