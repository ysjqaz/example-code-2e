# Norvig 的原版及更新版本

本目录包含：

* `original/`：
Norvig 的 [`lis.py`](https://github.com/norvig/pytudes/blob/c33cd6835a506a57d9fe73e3a8317d49babb13e8/py/lis.py)、
[`lispy.py`](https://github.com/norvig/pytudes/blob/c33cd6835a506a57d9fe73e3a8317d49babb13e8/py/lispy.py)，以及用于测试这两者的 `lispytest.py` 自定义测试脚本；
* `py3.10/`：带类型提示（type hint）、模式匹配（pattern matching）以及少量改动的 `lis.py`——需要 Python 3.10。

`py3.10/` 目录还包含 `lis_test.py`，可用
[pytest](https://docs.pytest.org) 运行，其中包含来自 `original/lispytest.py` 的
[`lis_tests` 测试集](https://github.com/norvig/pytudes/blob/60168bce8cdfacf57c92a5b2979f0b2e95367753/py/lispytest.py#L5)，
以及针对 `evaluate` 处理的每种表达式和特殊形式（special form）的额外独立测试。


## 出处、版权与许可

`lis.py`
[发布](https://github.com/norvig/pytudes/blob/c33cd6835a506a57d9fe73e3a8317d49babb13e8/py/lis.py)
在 Github 的 [norvig/pytudes](https://github.com/norvig/pytudes) 仓库中。
版权所有者为 Peter Norvig，代码采用
[MIT 许可证](https://github.com/norvig/pytudes/blob/60168bce8cdfacf57c92a5b2979f0b2e95367753/LICENSE) 授权。


## 对 Norvig 代码的改动

我对 `original/` 中的程序做了少量改动：

* 在 `lis.py` 中：
  * `Procedure` 类接受一个表达式列表作为 `body`，`__call__` 会依次对这些表达式求值，并返回最后一个表达式的值。这与 Scheme 的 `lambda` 语法一致，也为模式匹配提供了一个有用的示例。
  * 在 `'lambda'` 的 `elif` 分支中，我在元组解包时为 `*body` 变量加上了 `*`，以便将表达式收集为列表，再传给 `Procedure` 构造器。

* 在 `lispy.py` 中，我做了一些[改动并提交了 pull request](https://github.com/norvig/pytudes/pull/106)，使其能在 Python 3 上运行。

_Luciano Ramalho<br/>2021 年 6 月 29 日_
