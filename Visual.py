"""
Программа с удобным словарём через атрибуты и функциями для физуализации
"""
import matplotlib.pyplot as plt
import Geometry as g
from collections import UserDict


class Usefuldict(UserDict):
    def __init__(self, **kwargs):
        super().__setattr__('data', {})
        for key, value in kwargs.items():
            self.data[key] = value

    def __setitem__(self, key, value):
        self.data[key] = value

    def __setattr__(self, key, value):
        # if key == 'data':
        #     self.__dict__[key] = value
        self.data[key] = value

    def __getattr__(self, item):
        if item == 'data':
            return self.__dict__['data']
        return self.data[item]

    def values(self):
        return self.data.values()


def print_line_2p(ax, p1: g.Point, p2: g.Point, color='black'):
    ax.plot([p1.x, p2.x], [p1.y, p2.y], color=color)

def print_polygone(ax, points: list, color='black', endpoints=True) -> None:
    for i in range(len(points) - 1):
        print_line_2p(ax, points[i], points[i + 1], color=color)
    if endpoints:
        print_line_2p(ax, points[-1], points[0], color=color)
