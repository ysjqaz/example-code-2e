"""
示例改编自 Bruce Eckel 与 Svetlana Isakova 所著 `Atomic Kotlin`，
`Creating Generics` 章的 `Variance` 节。
"""

from typing import TYPE_CHECKING

from petbox import *


cat_box: Box[Cat] = Box()

si = Siamese()

cat_box.put(si)

animal = cat_box.get()

# if TYPE_CHECKING:
#    reveal_type(animal)  # 推断出的类型：petbox.Cat*


################### 协变（covariance）

out_box: OutBox[Cat] = OutBox(Cat())

out_box_si: OutBox[Siamese] = OutBox(Siamese())

out_box = out_box_si

## 赋值时类型不兼容
##   表达式类型为 "OutBox[Cat]"
##     变量类型为 "OutBox[Siamese]"
# out_box_si = out_box

################### 逆变（contravariance）

in_box: InBox[Cat] = InBox()

in_box_si: InBox[Siamese] = InBox()

## 赋值时类型不兼容
##   表达式类型为 "InBox[Siamese]"
##     变量类型为 "InBox[Cat]"
# in_box = in_box_si

in_box_si = in_box
