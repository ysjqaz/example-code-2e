import warnings

class metaMetaBunch(type):
    """
    新版改良版 "Bunch" 的元类（metaclass）：根据类作用域中绑定的变量
    隐式定义 __slots__、__init__ 和 __repr__。

    metaMetaBunch 实例（即以 metaMetaBunch 为元类的类）只能定义
    类作用域变量（以及可能存在的特殊方法，但不能是 __init__ 和 __repr__！）。
    metaMetaBunch 会把这些变量从类作用域中移除，改放到名为 __dflts__ 的
    类作用域 dict 中作为条目；并在类里放入一个 __slots__（列出这些变量的名字）、
    一个 __init__（把这些变量作为可选关键字参数，缺省时用 __dflts__ 中的值）、
    以及一个 __repr__（只展示与默认值不同的那些属性的 repr。
    按照惯例，__repr__ 的输出可以传给 __eval__ 来构造一个相等的实例）。
    """

    def __new__(cls, classname, bases, classdict):
        """ 一切都必须在 __new__ 中完成，因为 type.__new__
            才会处理 __slots__。
        """

        # 把新类要用的 __init__ 和 __repr__ 定义为局部函数

        def __init__(self, **kw):
            """ 简单的 __init__：先把所有属性设为默认值，
                再用 kw 中显式传入的值覆盖。
            """
            for k in self.__dflts__: setattr(self, k, self.__dflts__[k])
            for k in kw: setattr(self, k, kw[k])

        def __repr__(self):
            """ 巧妙的 __repr__：只展示与各自默认值不同的属性，
                以求简洁。
            """
            rep = [ '%s=%r' % (k, getattr(self, k)) for k in self.__dflts__
                    if getattr(self, k) != self.__dflts__[k]
                  ]
            return '%s(%s)' % (classname, ', '.join(rep))

        # 构造 newdict，作为新类的类字典
        newdict = { '__slots__':[], '__dflts__':{},
            '__init__':__init__, '__repr__':__repr__, }

        for k in classdict:
            if k.startswith('__'):
                # 特殊方法等：复制到 newdict，冲突时警告
                if k in newdict:
                    warnings.warn("Can't set attr %r in bunch-class %r" % (
                        k, classname))
                else:
                    newdict[k] = classdict[k]
            else:
                # 类变量：把名字存入 __slots__，
                # 把名字和值作为条目存入 __dflts__
                newdict['__slots__'].append(k)
                newdict['__dflts__'][k] = classdict[k]

        # 最后把剩余工作交给 type.__new__
        return type.__new__(cls, classname, bases, newdict)


class MetaBunch(metaclass=metaMetaBunch):
    """ 为方便起见：继承 MetaBunch 即可获得新的元类
        （等同于你自己定义 __metaclass__）。
    """
    __metaclass__ = metaMetaBunch
