

"""
覆盖型描述符（overriding descriptor，又称数据描述符（data descriptor）或强制描述符（enforced descriptor））：

    >>> obj = Model()
    >>> obj.over  # doctest: +ELLIPSIS
    Overriding.__get__() invoked with args:
        self     = <descriptorkinds.Overriding object at 0x...>
        instance = <descriptorkinds.Model object at 0x...>
        owner    = <class 'descriptorkinds.Model'>
    >>> Model.over  # doctest: +ELLIPSIS
    Overriding.__get__() invoked with args:
        self     = <descriptorkinds.Overriding object at 0x...>
        instance = None
        owner    = <class 'descriptorkinds.Model'>


覆盖型描述符无法通过对实例赋值来遮蔽：

    >>> obj = Model()
    >>> obj.over = 7  # doctest: +ELLIPSIS
    Overriding.__set__() invoked with args:
        self     = <descriptorkinds.Overriding object at 0x...>
        instance = <descriptorkinds.Model object at 0x...>
        value    = 7
    >>> obj.over  # doctest: +ELLIPSIS
    Overriding.__get__() invoked with args:
        self     = <descriptorkinds.Overriding object at 0x...>
        instance = <descriptorkinds.Model object at 0x...>
        owner    = <class 'descriptorkinds.Model'>


即使把属性塞进实例的 ``__dict__`` 也无法遮蔽：

    >>> obj.__dict__['over'] = 8
    >>> obj.over  # doctest: +ELLIPSIS
    Overriding.__get__() invoked with args:
        self     = <descriptorkinds.Overriding object at 0x...>
        instance = <descriptorkinds.Model object at 0x...>
        owner    = <class 'descriptorkinds.Model'>
    >>> vars(obj)
    {'over': 8}

没有 ``__get__`` 的覆盖型描述符：

    >>> obj.over_no_get  # doctest: +ELLIPSIS
    <descriptorkinds.OverridingNoGet object at 0x...>
    >>> Model.over_no_get   # doctest: +ELLIPSIS
    <descriptorkinds.OverridingNoGet object at 0x...>
    >>> obj.over_no_get = 7  # doctest: +ELLIPSIS
    OverridingNoGet.__set__() invoked with args:
        self     = <descriptorkinds.OverridingNoGet object at 0x...>
        instance = <descriptorkinds.Model object at 0x...>
        value    = 7
    >>> obj.over_no_get  # doctest: +ELLIPSIS
    <descriptorkinds.OverridingNoGet object at 0x...>


把属性塞进实例的 ``__dict__`` 意味着你可以读到该属性的新值，
但对它赋值仍然会触发 ``__set__``：

    >>> obj.__dict__['over_no_get'] = 9
    >>> obj.over_no_get
    9
    >>> obj.over_no_get = 7  # doctest: +ELLIPSIS
    OverridingNoGet.__set__() invoked with args:
        self     = <descriptorkinds.OverridingNoGet object at 0x...>
        instance = <descriptorkinds.Model object at 0x...>
        value    = 7
    >>> obj.over_no_get
    9


非覆盖型描述符（non-overriding descriptor，又称非数据描述符（non-data descriptor）或可遮蔽描述符（shadowable descriptor））：

    >>> obj = Model()
    >>> obj.non_over  # doctest: +ELLIPSIS
    NonOverriding.__get__() invoked with args:
        self     = <descriptorkinds.NonOverriding object at 0x...>
        instance = <descriptorkinds.Model object at 0x...>
        owner    = <class 'descriptorkinds.Model'>
    >>> Model.non_over  # doctest: +ELLIPSIS
    NonOverriding.__get__() invoked with args:
        self     = <descriptorkinds.NonOverriding object at 0x...>
        instance = None
        owner    = <class 'descriptorkinds.Model'>


非覆盖型描述符可以通过对实例赋值来遮蔽：

    >>> obj.non_over = 7
    >>> obj.non_over
    7


方法是非覆盖型描述符：

    >>> obj.spam  # doctest: +ELLIPSIS
    <bound method Model.spam of <descriptorkinds.Model object at 0x...>>
    >>> Model.spam  # doctest: +ELLIPSIS
    <function Model.spam at 0x...>
    >>> obj.spam()  # doctest: +ELLIPSIS
    Model.spam() invoked with arg:
        self = <descriptorkinds.Model object at 0x...>
    >>> obj.spam = 7
    >>> obj.spam
    7


任何类型的描述符都经不住在类本身上被覆盖：

    >>> Model.over = 1
    >>> obj.over
    1
    >>> Model.over_no_get = 2
    >>> obj.over_no_get
    2
    >>> Model.non_over = 3
    >>> obj.non_over
    7

"""

# BEGIN DESCRIPTORKINDS
def print_args(name, *args):  # <1>
    cls_name = args[0].__class__.__name__
    arg_names = ['self', 'instance', 'owner']
    if name == 'set':
        arg_names[-1] = 'value'
    print('{}.__{}__() invoked with args:'.format(cls_name, name))
    for arg_name, value in zip(arg_names, args):
        print('    {:8} = {}'.format(arg_name, value))


class Overriding:  # <2>
    """又称数据描述符（data descriptor）或强制描述符（enforced descriptor）"""

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)  # <3>

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class OverridingNoGet:  # <4>
    """一个没有 ``__get__`` 的覆盖型描述符"""

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class NonOverriding:  # <5>
    """又称非数据描述符（non-data descriptor）或可遮蔽描述符（shadowable descriptor）"""

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)


class Model:  # <6>
    over = Overriding()
    over_no_get = OverridingNoGet()
    non_over = NonOverriding()

    def spam(self):  # <7>
        print('Model.spam() invoked with arg:')
        print('    self =', self)

#END DESCRIPTORKINDS
