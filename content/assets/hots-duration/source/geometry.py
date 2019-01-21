from __future__ import annotations
from dataclasses import dataclass
from math import atan2, cos, sin, pi
from typing import List


@dataclass
class Point:
    x: float
    y: float
    z: float = 0

    def __add__(self, other: Point) -> Point:
        p = self.copy()
        p.x += other.x
        p.y += other.y
        p.z += other.z
        return p

    def __sub__(self, other: Point) -> Point:
        p = self.copy()
        p.x -= other.x
        p.y -= other.y
        p.z -= other.z
        return p

    def __mul__(self, factor: float) -> Point:
        p = self.copy()
        p.x *= factor
        p.y *= factor
        p.z *= factor
        return p

    def copy(self) -> Point:
        return Point(self.x, self.y, self.z)

    def angle_2D(self, other: Point) -> float:
        dx = other.x - self.x
        dy = other.y - self.y
        return atan2(dy, dx)

    def distance_2D(self, other: Point) -> float:
        return ((self.x - other.x)**2 + (self.y - other.y)**2) ** 0.5


@dataclass
class CubicBezierCurve:
    start: Point
    start_control: Point
    end_control: Point
    end: Point

    @property
    def points(self) -> List[Point]:
        return [
            self.start,
            self.start_control,
            self.end_control,
            self.end,
        ]

    def copy(self) -> CubicBezierCurve:
        return CubicBezierCurve(*[p.copy() for p in self.points])
