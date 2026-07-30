Sample code for Chapter 10 - "Design patterns with first class functions"

第十章「设计模式：一等函数」示例代码

选自 Luciano Ramalho 所著《Fluent Python》（O'Reilly, 2015）
http://shop.oreilly.com/product/0636920032519.do

说明
=====

无类型提示的文件不会报错
--------------------------------------

对第一版的 ``classic_strategy.py``（没有任何类型提示）运行 Mypy::

    $ mypy classic_strategy.py 
    Success: no issues found in 1 source file


类型推断在起作用
----------------------

当 ``Order.due`` 方法首次给 discount 赋值为 ``discount = 0`` 时，
Mypy 会抱怨::

    mypy classic_strategy.py 
    classic_strategy.py:68: error: Incompatible types in assignment (expression has type "float", variable has type "int")
    Found 1 error in 1 file (checked 1 source file)

为修正这个问题，我把首次赋值改为 ``discount = 0``。
我从未显式声明 ``discount`` 的类型。


Mypy 会忽略没有注解的函数
------------------------------------------

Mypy 不会对下面这个测试用例报错::


    def test_bulk_item_promo_with_discount(customer_fidelity_0):
        cart = [LineItem('banana', 30, .5),
                LineItem('apple', 10, 1.5)]
        order = Order(customer_fidelity_0, 10, BulkItemPromo())
        assert order.total() == 30.0
        assert order.due() == 28.5


``Order`` 的第二个参数声明为 ``Sequence[LineItem]``。
Mypy 只在函数签名至少包含一个注解时才检查函数体，
像这样::

    def test_bulk_item_promo_with_discount(customer_fidelity_0) -> None:
        cart = [LineItem('banana', 30, .5),
                LineItem('apple', 10, 1.5)]
        order = Order(customer_fidelity_0, 10, BulkItemPromo())
        assert order.total() == 30.0
        assert order.due() == 28.5


现在 Mypy 会抱怨 "Argument 2 of Order has incompatible type"。

然而，即便测试函数签名里有注解，
当我把 ``cart`` 参数的名字写错时，Mypy 也没发现任何问题。
这里 ``cart_plain`` 本应是 ``cart``::


    def test_bulk_item_promo_with_discount(customer_fidelity_0) -> None:
        cart = [LineItem('banana', 30, .5),
                LineItem('apple', 10, 1.5)]
        order = Order(customer_fidelity_0, cart_plain, BulkItemPromo())
        assert order.total() == 30.0
        assert order.due() == 28.5


假设：``cart_plain`` 是一个被 ``@pytest.fixture`` 装饰的函数，
而且在测试文件顶部我让 Mypy 忽略了 Pytest 的导入::

    import pytest  # type: ignore
