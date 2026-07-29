from collections.abc import Collection, Sequence

col_int: Collection[int]

seq_int: Sequence[int] = (1, 2, 3)

## 赋值时类型不兼容
##   表达式类型为 "Collection[int]"
##     变量类型为 "Sequence[int]"
# seq_int = col_int

col_int = seq_int

## 列表第 0 项类型不兼容："float"
##   期望 "int"
# col_int = [1.1]
