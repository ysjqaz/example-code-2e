from typing import TypeVar, Generic


class Beverage:
    """任意饮料。"""


class Juice(Beverage):
    """任意果汁。"""


class OrangeJuice(Juice):
    """用巴西橙子做的美味果汁。"""


T_co = TypeVar('T_co', covariant=True)


class BeverageDispenser(Generic[T_co]):
    def __init__(self, beverage: T_co) -> None:
        self.beverage = beverage

    def dispense(self) -> T_co:
        return self.beverage


class Garbage:
    """任意垃圾。"""


class Biodegradable(Garbage):
    """可生物降解的垃圾。"""


class Compostable(Biodegradable):
    """可堆肥的垃圾。"""


T_contra = TypeVar('T_contra', contravariant=True)


class TrashCan(Generic[T_contra]):
    def put(self, trash: T_contra) -> None:
        """存放垃圾直到倾倒。"""


class Cafeteria:
    def __init__(
        self,
        dispenser: BeverageDispenser[Juice],
        trash_can: TrashCan[Biodegradable],
    ):
        """初始化……"""


################################################ 精确类型

juice_dispenser = BeverageDispenser(Juice())
bio_can: TrashCan[Biodegradable] = TrashCan()

arnold_hall = Cafeteria(juice_dispenser, bio_can)


################################################ 协变的饮料分配器

orange_juice_dispenser = BeverageDispenser(OrangeJuice())

arnold_hall = Cafeteria(orange_juice_dispenser, bio_can)


################################################ 非协变的饮料分配器

beverage_dispenser = BeverageDispenser(Beverage())

## 传给 "Cafeteria" 的第 1 个参数
## 类型不兼容："BeverageDispenser[Beverage]"
##          期望 "BeverageDispenser[Juice]"
# arnold_hall = Cafeteria(beverage_dispenser, bio_can)


################################################ 逆变的垃圾桶

trash_can: TrashCan[Garbage] = TrashCan()

arnold_hall = Cafeteria(juice_dispenser, trash_can)


################################################ 非逆变的垃圾桶

compost_can: TrashCan[Compostable] = TrashCan()

## 传给 "Cafeteria" 的第 2 个参数
## 类型不兼容："TrashCan[Compostable]"
##          期望 "TrashCan[Biodegradable]"
# arnold_hall = Cafeteria(juice_dispenser, compost_can)
