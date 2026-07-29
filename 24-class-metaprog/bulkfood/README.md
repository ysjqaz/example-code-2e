# Legacy Class Descriptor and Metaclass Examples

# 遗留的类描述符与元类示例

这些示例取自《Fluent Python》第一版第 21 章「Class Metaprogramming」，
在《Fluent Python》第二版第 25 章「Class Metaprogramming」中也有提及。

这些示例是用 Python 3.4 开发的。
它们在 Python 3.9 下能正确运行，但如今不依赖类装饰器（decorator）或元类（metaclass）
也能更轻松地满足同样的需求。

这里保留它们，作为你可能在中遗留代码里见到的类元编程技术示例；
这类代码可以用实现了 `__set_name__` 的基类配合 `__init_subclass__` 与装饰器
重构为更简洁的形式。

## 建议练习

如果你想练习《Fluent Python》第二版第 24 章和第 25 章介绍的概念，
可以对最进阶的示例 `model_v8.py` 做如下改造：

1. 通过实现 `__set_name__` 来简化 `AutoStorage` 描述符（descriptor）。
   这样你也能简化 `EntityMeta` 元类。

2. 重写 `Entity` 类，用 `__init_subclass__` 取代 `EntityMeta` 元类——之后你就可以把 `EntityMeta` 删掉了。

`bulkfood_v8.py` 的代码无需改动，其中的 doctest 仍应通过。

重构时为了便于跑 doctest，常方便地加上 `-f` 选项，
让测试运行器在第一个失败的测试处即退出：

```
$ python3 -m doctest -f bulkfood_v8.py
```

祝你玩得开心！
