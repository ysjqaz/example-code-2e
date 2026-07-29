Sample code for Chapter 10 - "Design patterns with first class functions"

# 第十章 — 设计模式：一等函数

选自《Fluent Python》第 2 版，作者 Luciano Ramalho（O'Reilly, 2015）
http://shop.oreilly.com/product/0636920032519.do

Notes
=====

No issues on file with zero type hints
--------------------------------------

对第一版中没有类型提示（type hint）的 ``classic_strategy.py`` 运行 Mypy 检查::

    $ mypy classic_strategy.py
    Success: no issues found in 1 source file


Type inference at play
----------------------

当 ``Order.due`` 方法把 ``discount`` 的第一次赋值写成 ``discount = 0`` 时，
Mypy 抱怨了::

    mypy classic_strategy.py
    classic_strategy.py:68: error: Incompatible types in assignment (expression has type "float", variable has type "int")
    Found 1 error in 1 file (checked 1 source file)

为修复这个问题，我把第一次赋值改为 ``discount = 0``。
我从未为 ``discount`` 显式声明类型。


Mypy ignores functions with no annotations
------------------------------------------

Mypy 没有对下面这个测试用例提出任何问题::


    def test_bulk_item_promo_with_discount(customer_fidelity_0):
        cart = [LineItem('banana', 30, .5),
                LineItem('apple', 10, 1.5)]
        order = Order(customer_fidelity_0, 10, BulkItemPromo())
        assert order.total() == 30.0
        assert order.due() == 28.5


``Order`` 的第二个参数声明为 ``Sequence[LineItem]``。
Mypy 只在函数签名至少有一个注解（annotation）时才会检查函数体，
例如这样::

    def test_bulk_item_promo_with_discount(customer_fidelity_0) -> None:
        cart = [LineItem('banana', 30, .5),
                LineItem('apple', 10, 1.5)]
        order = Order(customer_fidelity_0, 10, BulkItemPromo())
        assert order.total() == 30.0
        assert order.due() == 28.5


此时 Mypy 会抱怨 "Argument 2 of Order has incompatible type"。

然而，即便测试函数签名里有了注解，当我把 ``cart`` 参数名拼错时
Mypy 也发现不了。下面 ``cart_plain`` 应该是 ``cart``::


    def test_bulk_item_promo_with_discount(customer_fidelity_0) -> None:
        cart = [LineItem('banana', 30, .5),
                LineItem('apple', 10, 1.5)]
        order = Order(customer_fidelity_0, cart_plain, BulkItemPromo())
        assert order.total() == 30.0
        assert order.due() == 28.5


假设（Hypotesis）：``cart_plain`` 是一个被 ``@pytest.fixture`` 装饰（decorator）
的函数，且在测试文件顶部我已经告诉 Mypy 忽略 Pytest 的导入::

    import pytest  # type: ignore
