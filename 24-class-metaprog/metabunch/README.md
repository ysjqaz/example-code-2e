# Examples from Python in a Nutshell, 3rd edition

# 《Python in a Nutshell（第 3 版）》示例

`original/bunch.py` 中的 `MetaBunch` 元类（metaclass）示例，
是 Alex Martelli、Anna Ravenscroft 和 Steve Holden 所著
[《Python in a Nutshell, 3rd edition》](https://learning.oreilly.com/library/view/python-in-a/9781491913833)
第 4 章「Object Oriented Python」中「How a Metaclass Creates a Class」一节
最后一个示例的原样拷贝。

`pre3.6/bunch.py` 版本做了一点简化：利用 Python 3 的 `super()`，并去掉了注释和 docstring，
便于与 `from3.6` 版本对比。

`from3.6/bunch.py` 版本进一步利用 Python 3.6 起保序的 `dict` 做了简化，
并做了其他精简，例如在 `__init__` 和 `__repr__` 中利用闭包（closure），
避免在类上加一个 `__defaults__` 映射。

三个版本的外部行为完全一致，
三个目录下的测试文件 `bunch_test.py` 内容也完全相同。
