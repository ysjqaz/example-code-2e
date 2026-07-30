#!/usr/bin/env jython
# 注意：截至 2020 年底，Jython 仍是 Python 2.7

"""
在 Jython 注册表文件中有这样一行：

python.security.respectJavaAccessibility = true

将其设为 false 后，Jython 就能访问 Java 对象的非公共
字段、方法和构造器。
"""

import Confidential

message = Confidential('top secret text')
for name in dir(message):
    attr = getattr(message, name)
    if not callable(attr):  # 仅非方法
        print name + '\t=', attr
