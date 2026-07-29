# tag::BEVERAGE_TYPES[]
from typing import TypeVar, Generic

class Beverage:  # <1>
    """任意饮料。"""

class Juice(Beverage):
    """任意果汁。"""

class OrangeJuice(Juice):
    """用巴西橙子做的美味果汁。"""

T = TypeVar('T')  # <2>

class BeverageDispenser(Generic[T]):  # <3>
    """按饮料类型参数化的分配器。"""
    def __init__(self, beverage: T) -> None:
        self.beverage = beverage

    def dispense(self) -> T:
        return self.beverage

def install(dispenser: BeverageDispenser[Juice]) -> None:  # <4>
    """安装一个果汁分配器。"""
# end::BEVERAGE_TYPES[]

################################################ 精确类型

# tag::INSTALL_JUICE_DISPENSER[]
juice_dispenser = BeverageDispenser(Juice())
install(juice_dispenser)
# end::INSTALL_JUICE_DISPENSER[]


################################################ 变型分配器

# tag::INSTALL_BEVERAGE_DISPENSER[]
beverage_dispenser = BeverageDispenser(Beverage())
install(beverage_dispenser)
## mypy: 传给 "install" 的第 1 个参数
## 类型不兼容："BeverageDispenser[Beverage]"
##          期望 "BeverageDispenser[Juice]"
# end::INSTALL_BEVERAGE_DISPENSER[]


################################################ 变型分配器

# tag::INSTALL_ORANGE_JUICE_DISPENSER[]
orange_juice_dispenser = BeverageDispenser(OrangeJuice())
install(orange_juice_dispenser)
## mypy: 传给 "install" 的第 1 个参数
## 类型不兼容："BeverageDispenser[OrangeJuice]"
##          期望 "BeverageDispenser[Juice]"
# end::INSTALL_ORANGE_JUICE_DISPENSER[]
