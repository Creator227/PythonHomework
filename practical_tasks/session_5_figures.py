from abc import abstractmethod, ABCMeta
import math


class GeometricFigure(metaclass= ABCMeta):
    @abstractmethod
    def perimeter(self):
        pass

    @abstractmethod
    def square(self):
        pass


class Circle(GeometricFigure):

    def __init__(self, radius: int):
        self.radius = radius

    def perimeter(self):
        return 2 * math.pi * self.radius

    def square(self):
        return math.pi * self.radius**2


class Rectangle(GeometricFigure):

    def __init__(self, width: int, length: int):
        self.width = width
        self.length = length

    def perimeter(self):
        return (self.width + self.length) * 2

    def square(self):
        return self.width + self.length

    def diagonal(self):
        return math.sqrt(self.width**2 * self.length**2)

    def fits_in_circle(self, circle_radius: int):
        return True if self.diagonal() <= 2*circle_radius else False


