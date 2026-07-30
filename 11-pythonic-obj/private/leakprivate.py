#!/usr/bin/env jython
# 注意：截至 2020 年底，Jython 仍是 Python 2.7

from java.lang.reflect import Modifier
import Confidential

message = Confidential('top secret text')
fields = Confidential.getDeclaredFields()
for field in fields:
    # 仅列出私有字段
    if Modifier.isPrivate(field.getModifiers()):
        field.setAccessible(True) # 破除访问限制
        print 'field:', field
        print '\t', field.getName(), '=', field.get(message)
