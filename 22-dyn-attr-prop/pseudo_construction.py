# 对象构造过程的伪代码
def make(the_class, some_arg):
    new_object = the_class.__new__(some_arg)
    if isinstance(new_object, the_class):
        the_class.__init__(new_object, some_arg)
    return new_object

# 下面两条语句大致等价
x = Foo('bar')
x = make(Foo, 'bar')
