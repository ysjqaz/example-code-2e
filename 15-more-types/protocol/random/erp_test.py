from typing import TYPE_CHECKING

from erp import EnterpriserRandomPopper
import randompop


def test_issubclass() -> None:
    assert issubclass(EnterpriserRandomPopper, randompop.RandomPopper)


def test_isinstance_untyped_items_argument() -> None:
    items = [1, 2, 3]
    popper = EnterpriserRandomPopper(items)  # 不需要写 [int]
    if TYPE_CHECKING:
        reveal_type(popper)
        # 推断出的类型为 'erp.EnterpriserRandomPopper[builtins.int*]'
    assert isinstance(popper, randompop.RandomPopper)


def test_isinstance_untyped_items_in_var_type() -> None:
    items = [1, 2, 3]
    popper: EnterpriserRandomPopper = EnterpriserRandomPopper[int](items)
    if TYPE_CHECKING:
        reveal_type(popper)
        # 推断出的类型为 'erp.EnterpriserRandomPopper[Any]'
    assert isinstance(popper, randompop.RandomPopper)


def test_isinstance_item() -> None:
    items = [1, 2, 3]
    popper = EnterpriserRandomPopper[int](items)  # 不需要写 [int]
    popped = popper.pop_random()
    if TYPE_CHECKING:
        reveal_type(popped)
        # 推断出的类型为 'builtins.int*'
    assert isinstance(popped, int)
