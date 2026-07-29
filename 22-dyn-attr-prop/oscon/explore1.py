"""
explore1.py：用于探索 OSCON 日程数据的脚本

    >>> import json
    >>> raw_feed = json.load(open('data/osconfeed.json'))
    >>> feed = FrozenJSON(raw_feed)
    >>> len(feed.Schedule.speakers)
    357
    >>> sorted(feed.Schedule.keys())
    ['conferences', 'events', 'speakers', 'venues']
    >>> for key, value in sorted(feed.Schedule.items()):
    ...     print(f'{len(value):3} {key}')
    ...
      1 conferences
    484 events
    357 speakers
     53 venues
    >>> feed.Schedule.speakers[-1].name
    'Carina C. Zona'
    >>> talk = feed.Schedule.events[40]
    >>> type(talk)
    <class 'explore1.FrozenJSON'>
    >>> talk.name
    'There *Will* Be Bugs'
    >>> talk.speakers
    [3471, 5199]
    >>> talk.flavor
    Traceback (most recent call last):
      ...
    KeyError: 'flavor'

通过追加一个 `_` 来处理关键字。

# tag::EXPLORE1_DEMO[]

    >>> grad = FrozenJSON({'name': 'Jim Bo', 'class': 1982})
    >>> grad.name
    'Jim Bo'
    >>> grad.class_
    1982

# end::EXPLORE1_DEMO[]

"""

from collections import abc
import keyword


class FrozenJSON:
    """一个只读门面（façade），用于以属性（attribute）记法
       在类 JSON 对象中导航
    """

# tag::EXPLORE1[]
    def __init__(self, mapping):
        self.__data = {}
        for key, value in mapping.items():
            if keyword.iskeyword(key):  # <1>
                key += '_'
            self.__data[key] = value
# end::EXPLORE1[]

    def __getattr__(self, name):
        try:
            return getattr(self.__data, name)
        except AttributeError:
            return FrozenJSON.build(self.__data[name])

    def __dir__(self):  # <5>
        return self.__data.keys()

    @classmethod
    def build(cls, obj):
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]
        else:  # <8>
            return obj

