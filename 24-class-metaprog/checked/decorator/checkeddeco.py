"""
``Checked`` 子类在定义时要求用关键字参数创建实例（instance），
并提供友好的 ``__repr__``::

# tag::MOVIE_DEFINITION[]

    >>> @checked
    ... class Movie:
    ...     title: str
    ...     year: int
    ...     box_office: float
    ...
    >>> movie = Movie(title='The Godfather', year=1972, box_office=137)
    >>> movie.title
    'The Godfather'
    >>> movie
    Movie(title='The Godfather', year=1972, box_office=137.0)

# end::MOVIE_DEFINITION[]

设置属性（包括实例化时）会对参数类型做运行时检查::

# tag::MOVIE_TYPE_VALIDATION[]

    >>> blockbuster = Movie(title='Avatar', year=2009, box_office='billions')
    Traceback (most recent call last):
      ...
    TypeError: 'billions' is not compatible with box_office:float
    >>> movie.year = 'MCMLXXII'
    Traceback (most recent call last):
      ...
    TypeError: 'MCMLXXII' is not compatible with year:int

# end::MOVIE_TYPE_VALIDATION[]

未作为参数传给构造器的属性会以默认值初始化::

# tag::MOVIE_DEFAULTS[]

    >>> Movie(title='Life of Brian')
    Movie(title='Life of Brian', year=0, box_office=0.0)

# end::MOVIE_DEFAULTS[]

不允许向构造器传入多余的参数::

    >>> blockbuster = Movie(title='Avatar', year=2009, box_office=2000,
    ...                     director='James Cameron')
    Traceback (most recent call last):
      ...
    AttributeError: 'Movie' has no attribute 'director'

运行时也不允许创建新属性::

    >>> movie.director = 'Francis Ford Coppola'
    Traceback (most recent call last):
      ...
    AttributeError: 'Movie' has no attribute 'director'

实例方法 `_asdict` 用 `Movie` 对象的属性构造一个 `dict`::

    >>> movie._asdict()
    {'title': 'The Godfather', 'year': 1972, 'box_office': 137.0}

"""

from collections.abc import Callable  # <1>
from typing import Any, NoReturn, get_type_hints

class Field:
    def __init__(self, name: str, constructor: Callable) -> None:  # <2>
        if not callable(constructor) or constructor is type(None):
            raise TypeError(f'{name!r} type hint must be callable')
        self.name = name
        self.constructor = constructor

    def __set__(self, instance: Any, value: Any) -> None:  # <3>
        if value is ...:  # <4>
            value = self.constructor()
        else:
            try:
                value = self.constructor(value)  # <5>
            except (TypeError, ValueError) as e:
                type_name = self.constructor.__name__
                msg = (
                    f'{value!r} is not compatible with {self.name}:{type_name}'
                )
                raise TypeError(msg) from e
        instance.__dict__[self.name] = value  # <6>


# tag::CHECKED_DECORATOR[]
def checked(cls: type) -> type:  # <1>
    for name, constructor in _fields(cls).items():    # <2>
        setattr(cls, name, Field(name, constructor))  # <3>

    cls._fields = classmethod(_fields)  # type: ignore  # <4>

    instance_methods = (  # <5>
        __init__,
        __repr__,
        __setattr__,
        _asdict,
        __flag_unknown_attrs,
    )
    for method in instance_methods:  # <6>
        setattr(cls, method.__name__, method)

    return cls  # <7>
# end::CHECKED_DECORATOR[]

# tag::CHECKED_METHODS[]
def _fields(cls: type) -> dict[str, type]:
    return get_type_hints(cls)

def __init__(self: Any, **kwargs: Any) -> None:
    for name in self._fields():
        value = kwargs.pop(name, ...)
        setattr(self, name, value)
    if kwargs:
        self.__flag_unknown_attrs(*kwargs)

def __setattr__(self: Any, name: str, value: Any) -> None:
    if name in self._fields():
        cls = self.__class__
        descriptor = getattr(cls, name)
        descriptor.__set__(self, value)
    else:
        self.__flag_unknown_attrs(name)

def __flag_unknown_attrs(self: Any, *names: str) -> NoReturn:
    plural = 's' if len(names) > 1 else ''
    extra = ', '.join(f'{name!r}' for name in names)
    cls_name = repr(self.__class__.__name__)
    raise AttributeError(f'{cls_name} has no attribute{plural} {extra}')

def _asdict(self: Any) -> dict[str, Any]:
    return {
        name: getattr(self, name)
        for name, attr in self.__class__.__dict__.items()
        if isinstance(attr, Field)
    }

def __repr__(self: Any) -> str:
    kwargs = ', '.join(
        f'{key}={value!r}' for key, value in self._asdict().items()
    )
    return f'{self.__class__.__name__}({kwargs})'
# end::CHECKED_METHODS[]
