#!/usr/bin/env python3

from typing import TYPE_CHECKING

# tag::LOTTO_USE[]
from generic_lotto import LottoBlower

machine = LottoBlower[int](range(1, 11))  # <1>

first = machine.pick()  # <2>
remain = machine.inspect()  # <3>
# end::LOTTO_USE[]

expected = set(i for i in range(1, 11) if i != first)

assert set(remain) == expected

print('picked:', first)
print('remain:', remain)

if TYPE_CHECKING:
    reveal_type(first)
    # 推断出的类型为 'builtins.int*'
if TYPE_CHECKING:
    reveal_type(remain)
    # 推断出的类型为 'builtins.tuple[builtins.int*]'


