# tag::TRASH_TYPES[]
from typing import TypeVar, Generic

class Refuse:  # <1>
    """任意废弃物。"""

class Biodegradable(Refuse):
    """可生物降解的废弃物。"""

class Compostable(Biodegradable):
    """可堆肥的废弃物。"""

T_contra = TypeVar('T_contra', contravariant=True)  # <2>

class TrashCan(Generic[T_contra]):  # <3>
    def put(self, refuse: T_contra) -> None:
        """存放垃圾直到倾倒。"""

def deploy(trash_can: TrashCan[Biodegradable]):
    """部署一个用于可生物降解废弃物的垃圾桶。"""
# end::TRASH_TYPES[]


################################################ 逆变的垃圾桶


# tag::DEPLOY_TRASH_CANS[]
bio_can: TrashCan[Biodegradable] = TrashCan()
deploy(bio_can)

trash_can: TrashCan[Refuse] = TrashCan()
deploy(trash_can)
# end::DEPLOY_TRASH_CANS[]


################################################ 更具体的垃圾桶

# tag::DEPLOY_NOT_VALID[]
compost_can: TrashCan[Compostable] = TrashCan()
deploy(compost_can)
## mypy: 传给 "deploy" 的第 1 个参数
## 类型不兼容："TrashCan[Compostable]"
##          期望 "TrashCan[Biodegradable]"
# end::DEPLOY_NOT_VALID[]
