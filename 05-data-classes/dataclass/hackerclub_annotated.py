# tag::DOCTESTS[]
"""
``HackerClubMember`` 对象可用 ``name`` 和一个可选的 ``handle`` 参数来创建::

    >>> anna = HackerClubMember('Anna Ravenscroft', handle='AnnaRaven')
    >>> anna
    HackerClubMember(name='Anna Ravenscroft', guests=[], handle='AnnaRaven')

如果省略 ``handle``，则取成员名的第一部分作为其值::

    >>> leo = HackerClubMember('Leo Rochael')
    >>> leo
    HackerClubMember(name='Leo Rochael', guests=[], handle='Leo')

成员必须拥有唯一的 handle。下面的 ``leo2`` 将无法被创建，
因为它的 ``handle`` 会是 'Leo'，而该值已被 ``leo`` 占用::

    >>> leo2 = HackerClubMember('Leo DaVinci')
    Traceback (most recent call last):
      ...
    ValueError: handle 'Leo' already exists.

要解决此问题，必须为 ``leo2`` 显式指定一个 ``handle``::

    >>> leo2 = HackerClubMember('Leo DaVinci', handle='Neo')
    >>> leo2
    HackerClubMember(name='Leo DaVinci', guests=[], handle='Neo')
"""
# end::DOCTESTS[]

# tag::HACKERCLUB[]
from dataclasses import dataclass
from typing import ClassVar
from club import ClubMember

@dataclass
class HackerClubMember(ClubMember):
    all_handles: ClassVar[set[str]] = set()
    handle: str = ''

    def __post_init__(self):
        cls = self.__class__
        if self.handle == '':
            self.handle = self.name.split()[0]
        if self.handle in cls.all_handles:
            msg = f'handle {self.handle!r} already exists.'
            raise ValueError(msg)
        cls.all_handles.add(self.handle)
# end::HACKERCLUB[]
