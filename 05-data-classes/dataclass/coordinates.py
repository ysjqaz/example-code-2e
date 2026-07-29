"""
``Coordinate``：用 ``dataclass`` 装饰、并带自定义 ``__str__`` 的简单类（class）::

    >>> moscow = Coordinate(55.756, 37.617)
    >>> print(moscow)
    55.8°N, 37.6°E

"""

# tag::COORDINATE[]

from dataclasses import dataclass

@dataclass(frozen=True)
class Coordinate:
    lat: float
    lon: float

    def __str__(self):
        ns = 'N' if self.lat >= 0 else 'S'
        we = 'E' if self.lon >= 0 else 'W'
        return f'{abs(self.lat):.1f}°{ns}, {abs(self.lon):.1f}°{we}'
# end::COORDINATE[]
