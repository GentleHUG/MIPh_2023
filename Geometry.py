"""
Программа с различными геометрическими объектами
"""
import math as m
from functools import total_ordering
from decimal import Decimal


class Point:
    def __init__(self, x: Decimal, y: Decimal) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __repr__(self):
        return f'{self.__class__.__name__}({self.x:.3f}, {self.y:.3f})'

    def __add__(self, other):
        if isinstance(other, tuple):
            return Point(self.x + other[0], self.y + other[1])
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, tuple):
            return Point(self.x - other[0], self.y - other[1])
        return NotImplemented

@total_ordering
class Angle:
    def __init__(self, value: Decimal, from_rad=True) -> None:
        if from_rad:
            self.rad = value
            self.deg = value / Decimal(m.pi) * 180
        else:
            self.rad = value / 180 * Decimal(m.pi)
            self.deg = value

    def __add__(self, other):
        if isinstance(other, Angle):
            return Angle(self.rad + other.rad)
        if isinstance(other, float):
            return Angle(self.rad + other)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Angle):
            return Angle(self.rad - other.rad)
        if isinstance(other, Decimal):
            return Angle(self.rad - other)
        return NotImplemented

    def __repr__(self) -> str:
        return f'Angle({self.rad:.3f} rad, {self.deg:.1f} deg)'

    def __eq__(self, other):
        if isinstance(other, Angle):
            return self.rad == other.rad
        if isinstance(other, Decimal):
            return self.rad == other
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Angle):
            return self.rad < other.rad
        if isinstance(other, Decimal):
            return self.rad < other
        return NotImplemented

    @property
    def cos(self) -> Decimal:
        return Decimal(m.cos(self.rad))

    @property
    def sin(self) -> Decimal:
        return Decimal(m.sin(self.rad))

    @property
    def tan(self) -> Decimal:
        return Decimal(m.tan(self.rad))


class Vector:
    def __init__(self, x: Decimal, y: Decimal):
        self.x = x
        self.y = y

        if x:
            self.angle = Angle(Decimal(m.atan(y/x)))
        else:
            self.angle = Angle(Decimal(m.pi/2))

    def modulo(self) -> Decimal:
        return Decimal(m.sqrt(self*self))

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x+other.x, self.y+other.y)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Vector):
            return self.x*other.x + self.y*other.y
        if isinstance(other, Decimal):
            return Vector(self.x*other, self.y*other)
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, Decimal):
            return Vector(self.x/other, self.y/other)
        raise ValueError('Can divide only on int or float')

    def __repr__(self):
        return f'Vector({self.x}, {self.y})'

    def normal(self):
        return Vector(self.y, -self.x) / self.modulo()

    def refraction_vector(self, normal, n1=Decimal(1), n2=Decimal(1)):
        v1 = self / self.modulo() * n1
        D = (n2**2-n1**2)/(v1*normal)**2+1
        if D >= 0:
            return v1 + normal*(D.sqrt()-1)*(v1*normal)
        raise ValueError('Refraction doesnt exist')





class Line:
    def __init__(self, a: Decimal, b: Decimal, c: Decimal = Decimal(0)) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.vec = Vector(b, -a)

    @staticmethod
    def from_points(point1: Point, point2: Point):
        vec = Vector(point2.x - point1.x, point2.y - point1.y)
        return Line.from_point_and_vec(point1, vec)

    @staticmethod
    def from_point_and_vec(point: Point, vec: Vector):
        return Line(vec.y, -vec.x, vec.x*point.y-vec.y*point.x)

    def refraction(self, border, n1: Decimal, n2: Decimal):
        if isinstance(border, Line):
            if isinstance(n1, Decimal) and isinstance(n2, Decimal):
                cross_point = self * border
                norm_vector = border.vec.normal()
                new_vec = self.vec.refraction_vector(norm_vector, n1, n2)
                return Line.from_point_and_vec(cross_point, new_vec)
            raise ValueError('Coof must be int or float')
        raise ValueError('Not line given')

    def __mul__(self, other) -> Point:
        if isinstance(other, Line):
            d = self.a*other.b-other.a*self.b
            d1 = -self.c*other.b+other.c*self.b
            d2 = -self.a*other.c+other.a*self.c
            if d:
                return Point(d1/d, d2/d)
            raise ZeroDivisionError('Lines never collide')
        raise ValueError('Not line given')

    def __or__(self, other) -> Angle:
        if isinstance(other, Line):
            prod = self.a*other.a+self.b*other.b
            if not prod:
                return Angle(Decimal(m.pi/2))
            return Angle(Decimal(m.acos(prod/((self.a**2+self.b**2).sqrt()*(other.a**2+other.b**2).sqrt()))))

    def __repr__(self):
        return f'Line({self.a}x+{self.b}y+{self.c}=0, {self.vec})'
