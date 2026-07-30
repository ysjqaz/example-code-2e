import abc


class AutoStorage:
    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = '_{}#{}'.format(prefix, index)
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)


class Validated(abc.ABC, AutoStorage):

    def __set__(self, instance, value):
        value = self.validate(instance, value)
        super().__set__(instance, value)

    @abc.abstractmethod
    def validate(self, instance, value):
        """返回验证后的值，或抛出 ValueError"""


class Quantity(Validated):
    """大于零的数字"""

    def validate(self, instance, value):
        if value <= 0:
            raise ValueError('value must be > 0')
        return value


class NonBlank(Validated):
    """至少包含一个非空白字符的字符串"""

    def validate(self, instance, value):
        value = value.strip()
        if len(value) == 0:
            raise ValueError('value cannot be empty or blank')
        return value

# tag::MODEL_V7[]
class EntityMeta(type):
    """带有验证字段的业务实体的元类（metaclass）"""

    def __init__(cls, name, bases, attr_dict):
        super().__init__(name, bases, attr_dict)  # <1>
        for key, attr in attr_dict.items():  # <2>
            if isinstance(attr, Validated):
                type_name = type(attr).__name__
                attr.storage_name = '_{}#{}'.format(type_name, key)

class Entity(metaclass=EntityMeta):  # <3>
    """带有验证字段的业务实体"""
# end::MODEL_V7[]
