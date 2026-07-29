"""
``Coordinate``：一个带自定义 ``__str__`` 的简单 ``NamedTuple``（具名元组）子类::

    >>> moscow = Coordinate(55.756, 37.617)
    >>> print(moscow)
    55.8°N, 37.6°E

"""

# tag::COORDINATE[]
from typing import NamedTuple

class Coordinate(NamedTuple):
    lat: float
    lon: float

    def __str__(self):
        ns = 'N' if self.lat >= 0 else 'S'
        we = 'E' if self.lon >= 0 else 'W'
        return f'{abs(self.lat):.1f}°{ns}, {abs(self.lon):.1f}°{we}'
# end::COORDINATE[]
