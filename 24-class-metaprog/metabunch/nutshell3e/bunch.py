import collections
import warnings

class MetaBunch(type):
    """
    新版改良版 "Bunch" 的元类（metaclass）：根据类作用域中绑定的变量
    隐式定义 __slots__、__init__ 和 __repr__。
    MetaBunch 实例（即以 MetaBunch 为元类的类）对应的 class 语句
    只能定义类作用域的数据属性（以及可能存在的特殊方法，
    但不能是 __init__ 和 __repr__）。MetaBunch 会把这些数据属性
    从类作用域中移除，改放到名为 __dflts__ 的类作用域 dict 中作为条目；
    并在类里放入一个 __slots__（列出这些属性的名字）、
    一个 __init__（把这些属性作为可选命名参数，缺省时用 __dflts__ 中的值）、
    以及一个 __repr__（只展示与默认值不同的那些属性的 repr。
    按照惯例，__repr__ 的输出可以传给 __eval__ 来构造一个相等的实例，
    前提是每个非默认值的属性也遵循这一惯例）。

    在 v3 中，数据属性的顺序与类体中的顺序保持一致；
    在 v2 中则没有这一保证。
    """
    def __prepare__(name, *bases, **kwargs):
        # 在 v3 中很珍贵——在 v2 中虽无用但也无害
        return collections.OrderedDict()

    def __new__(mcl, classname, bases, classdict):
        """ 一切都必须在 __new__ 中完成，因为 type.__new__
            才会处理 __slots__。
        """
        # 把新类要用的 __init__ 和 __repr__ 定义为局部函数
        def __init__(self, **kw):
            """ 简单的 __init__：先把所有属性设为默认值，
                再用 kw 中显式传入的值覆盖。
            """
            for k in self.__dflts__:
                setattr(self, k, self.__dflts__[k])
            for k in kw:
                setattr(self, k, kw[k])
        def __repr__(self):
            """ 巧妙的 __repr__：只展示与默认值不同的属性，
                以求简洁。
            """
            rep = ['{}={!r}'.format(k, getattr(self, k))
                    for k in self.__dflts__
                    if getattr(self, k) != self.__dflts__[k]
                  ]
            return '{}({})'.format(classname, ', '.join(rep))
        # 构造 newdict，作为新类的类字典
        newdict = { '__slots__':[],
            '__dflts__':collections.OrderedDict(),
            '__init__':__init__, '__repr__':__repr__, }
        for k in classdict:
            if k.startswith('__') and k.endswith('__'):
                # 双下方法：复制到 newdict，或在冲突时警告
                if k in newdict:
                    warnings.warn(
                        "Can't set attr {!r} in bunch-class {!r}".
                        format(k, classname))
                else:
                    newdict[k] = classdict[k]
            else:
                # 类变量：把名字存入 __slots__，
                # 把名字和值作为条目存入 __dflts__
                newdict['__slots__'].append(k)
                newdict['__dflts__'][k] = classdict[k]
        # 最后把剩余工作交给 type.__new__
        return super(MetaBunch, mcl).__new__(
                     mcl, classname, bases, newdict)

class Bunch(metaclass=MetaBunch):
    """ 为方便起见：继承 Bunch 即可获得新的元类
        （等同于你自己写 metaclass=）。

        在 v2 中，删掉上面的 (metaclass=MetaBunch)，
        改在类体里加 __metaclass__=MetaBunch。
    """
    pass
