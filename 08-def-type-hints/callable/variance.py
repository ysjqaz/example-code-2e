from collections.abc import Callable

def update(  # <1>
        probe: Callable[[], float],  # <2>
        display: Callable[[float], None]  # <3>
    ) -> None:
    temperature = probe()
    # 想象这里有很多控制代码
    display(temperature)

def probe_ok() -> int:  # <4>
    return 42

def display_wrong(temperature: int) -> None:  # <5>
    print(hex(temperature))

update(probe_ok, display_wrong)  # 类型错误  # <6>

def display_ok(temperature: complex) -> None:  # <7>
    print(temperature)

update(probe_ok, display_ok)  # 没问题  # <8>
