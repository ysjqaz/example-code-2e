from typing import TypeVar, Generic


class Beverage:
    """任意饮料。"""


class Juice(Beverage):
    """任意果汁。"""


class OrangeJuice(Juice):
    """用巴西橙子做的美味果汁。"""


# tag::BEVERAGE_TYPES[]
T_co = TypeVar('T_co', covariant=True)  # <1>


class BeverageDispenser(Generic[T_co]):  # <2>
    def __init__(self, beverage: T_co) -> None:
        self.beverage = beverage

    def dispense(self) -> T_co:
        return self.beverage

def install(dispenser: BeverageDispenser[Juice]) -> None:  # <3>
    """安装一个果汁分配器。"""
# end::BEVERAGE_TYPES[]

################################################ 协变的分配器

# tag::INSTALL_JUICE_DISPENSERS[]
juice_dispenser = BeverageDispenser(Juice())
install(juice_dispenser)

orange_juice_dispenser = BeverageDispenser(OrangeJuice())
install(orange_juice_dispenser)
# end::INSTALL_JUICE_DISPENSERS[]

################################################ 更泛化的分配器

# tag::INSTALL_BEVERAGE_DISPENSER[]
beverage_dispenser = BeverageDispenser(Beverage())
install(beverage_dispenser)
## mypy: 传给 "install" 的第 1 个参数
## 类型不兼容："BeverageDispenser[Beverage]"
##          期望 "BeverageDispenser[Juice]"
# end::INSTALL_BEVERAGE_DISPENSER[]
