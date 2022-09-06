from enum import Enum
from typing import Tuple, TypedDict

from colors import PygameColor

Coordinate = Tuple[int, int]
PxSize = Tuple[int, int]


class MovementDirection(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class RenderInfo(TypedDict):
    color: PygameColor
