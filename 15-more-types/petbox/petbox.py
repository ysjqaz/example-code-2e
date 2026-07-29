"""
示例改编自 Bruce Eckel 与 Svetlana Isakova 所著 `Atomic Kotlin`，
`Creating Generics` 章的 `Variance` 节。
"""

from typing import TypeVar, Generic, Any


class Pet:
    """作为伴侣饲养的家养动物。"""


class Cat(Pet):
    """Felis catus（猫）"""


class Siamese(Cat):
    """原产泰国的猫品种"""


T = TypeVar('T')


class Box(Generic[T]):
    def put(self, item: T) -> None:
        self.contents = item

    def get(self) -> T:
        return self.contents


T_co = TypeVar('T_co', covariant=True)


class OutBox(Generic[T_co]):
    def __init__(self, contents: Any):
        self.contents = contents

    def get(self) -> Any:
        return self.contents


T_contra = TypeVar('T_contra', contravariant=True)


class InBox(Generic[T_contra]):
    def put(self, item: T) -> None:
        self.contents = item
