# The Python Data Model

# 第一章 — Python 数据模型

《Fluent Python 2e》（Luciano Ramalho 著，O'Reilly，2020）第 1 章配套示例代码。

## 运行测试

### Doctest

使用 Python 标准库的 ``doctest`` 模块检查独立的 doctest 文件：

    $ python3 -m doctest frenchdeck.doctest -v

检查内嵌在模块中的 doctest：

    $ python3 -m doctest vector2d.py -v

### Jupyter Notebook

安装 ``pytest`` 和 ``nbval`` 插件：

    $ pip install pytest nbval

运行：

    $ pytest --nbval
