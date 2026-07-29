from generic_lotto import LottoBlower

machine = LottoBlower[int]([1, .2])
## 错误：列表第 1 项类型不兼容："float";  # <1>
##        期望 "int"

machine = LottoBlower[int](range(1, 11))

machine.load('ABC')
## 错误：传给 "LottoBlower" 的 "load" 的第 1 个参数  # <2>
##        类型不兼容："str";
##        期望 "Iterable[int]"
## 提示：  "str" 的以下成员存在冲突：
## 提示：      期望：
## 提示：          def __iter__(self) -> Iterator[int]
## 提示：      实际：
## 提示：          def __iter__(self) -> Iterator[str]

