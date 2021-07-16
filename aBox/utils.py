from dataclasses import dataclass
from enum import Enum, auto
from typing import Iterator


@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)
    
    def __neg__(self) -> "Point":
        return Point(-self.x, -self.y)

    def __iter__(self) -> Iterator[int]:
        return iter((self.x, self.y))


P = Point


class Action(Enum):
    move_up = auto()
    move_down = auto()
    move_left = auto()
    move_right = auto()
    grab_up = auto()
    grab_down = auto()
    grab_left = auto()
    grab_right = auto()
    ungrab = auto()
    wait = auto()
