import dataclasses as dto
from math import cos

from .models import Product


@dto.dataclass
class Point:
    lat: float
    lon: float

    def __add__(self, other):
        return Point(self.lat + other.lat, self.lon + other.lon)

    def __invert__(self):
        return Point(-self.lat, -self.lon)

    def __sub__(self, other):
        return self.__add__(other.__invert__())


def latitude_converter(lat): return lat / 110.57


def long_converter(lat, lon): return lon / (111.320 * cos(lat))


def min_max_points(point: Point, distance: float):
    dis_point = Point(latitude_converter(distance), long_converter(point.lat, distance))
    return point + dis_point, point - dis_point


def get_close_products(location_dict):
    location = Point(location_dict['latitude'], location_dict['longitude'])
    max_point, min_point = min_max_points(location, location_dict['distance_km'])
    products = Product.objects.filter(latitude__lte=max_point.lat,
                                      longitude__lte=max_point.lon,
                                      latitude__gte=min_point.lat,
                                      longitude__gte=min_point.lon)
    return products

