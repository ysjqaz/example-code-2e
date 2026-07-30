#!/usr/bin/env jython
# 注意：截至 2020 年底，Jython 仍是 Python 2.7

import Confidential

message = Confidential('top secret text')
secret_field = Confidential.getDeclaredField('secret')
secret_field.setAccessible(True)  # 破除访问限制！
print 'message.secret =', secret_field.get(message)
