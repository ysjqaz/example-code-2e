# 相对原版的改动

在将 Peter Norvig 的 [lis.py](https://github.com/norvig/pytudes/blob/705c0a335c1811a203e79587d7d41865cf7f41c7/py/lis.py) 改编用于《流畅的 Python（第二版）》时，出于教学目的我做了少量改动。

_Luciano Ramalho_

## 主要改动

* 让 `lambda` 形式接受多个表达式作为函数体。这与 [_Scheme_ 语法](https://web.mit.edu/scheme_v9.2/doc/mit-scheme-ref/Lambda-Expressions.html)一致，也为本书提供了一个有用的示例。为此：
    * 在 `Procedure.__call__` 中：把 `self.body` 作为表达式列表求值，而不是单个表达式。返回最后一个表达式的值。
    * 在 `evaluate()` 中：处理 `lambda` 时，将表达式解包为 `(_, parms, *body)`，以接受多个表达式作为函数体。
* 移除 `global_env` 这个全局 `dict`。它原本只用作 `evaluate()` 中 `env` 参数的默认值，但把可变数据结构作为参数默认值是不安全的。为此：
    * 在 `repl()` 中：创建局部变量 `global_env`，并将其作为 `evaluate()` 的 `env` 参数传入。
    * 在 `evaluate()` 中：移除 `env` 的 `global_env` 默认值。
* 把自定义测试脚本
[lispytest.py](https://github.com/norvig/pytudes/blob/705c0a335c1811a203e79587d7d41865cf7f41c7/py/lispytest.py) 重写为
[lis_test.py](https://github.com/fluentpython/example-code-2e/blob/master/02-array-seq/lispy/py3.9/lis_test.py)：
一套标准的 [pytest](https://docs.pytest.org) 测试集，包含新的测试用例，同时保留了 Norvig 为
[lis.py](https://github.com/norvig/pytudes/blob/705c0a335c1811a203e79587d7d41865cf7f41c7/py/lis.py)
编写的全部测试用例，但移除了那些仅针对
[lispy.py](https://github.com/norvig/pytudes/blob/705c0a335c1811a203e79587d7d41865cf7f41c7/py/lispy.py)
所实现功能的测试用例。


## 次要改动

为了让代码看起来更亲切而做的表面改动，目标读者是《流畅的 Python》的读者——Python 程序员。

* 将 `eval()` 重命名为 `evaluate()`，以避免与 Python 内置函数 `eval` 混淆。
* 将列表类直接称为 `list`，而不是别名 `List`，以避免与常常被导入为 `List` 的 `typing.List` 混淆。
* 将 `collections.ChainMap` 作为 `ChainMap` 导入，而不是 `Environment`。
