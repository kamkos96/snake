import random

from colors import Colors
from common import Coordinate, MovementDirection, RenderInfo


class MapPoint:
    render: RenderInfo = {"color": Colors.JET_JET_JET}

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    @property
    def coord(self) -> Coordinate:
        return (self.x, self.y)

    def adjust_to_bounds(self, map) -> None:
        if self.x < 0:
            self.x = map.width - 1
        if self.x >= map.width:
            self.x = 0
        if self.y < 0:
            self.y = map.height - 1
        if self.y >= map.height:
            self.y = 0


class Snake:
    render: RenderInfo = {"color": Colors.WHITE}

    def __init__(self, initial_placement: MapPoint) -> None:
        self.positions: list[MapPoint] = [initial_placement]
        self.current_direction = MovementDirection.UP

    def set_current_direction(self, direction: MovementDirection) -> None:
        self.current_direction = direction

    def get_next_position(self) -> MapPoint:
        base: MapPoint = self.positions[0]
        match self.current_direction:
            case MovementDirection.UP:
                return MapPoint(base.x, base.y - 1)
            case MovementDirection.DOWN:
                return MapPoint(base.x, base.y + 1)
            case MovementDirection.LEFT:
                return MapPoint(base.x - 1, base.y)
            case MovementDirection.RIGHT:
                return MapPoint(base.x + 1, base.y)

    def move(self, next_pos: MapPoint, keep_last: bool = False) -> None:
        self.positions.insert(0, next_pos)
        if not keep_last:
            self.positions.pop()

    def eat_food(self, pos: MapPoint) -> None:
        self.move(pos, True)


class Food:
    render: RenderInfo = {"color": Colors.GREEN}

    def __init__(self, snake_positions: list[MapPoint], max_size: Coordinate) -> None:
        self.snake_positions: list[MapPoint] = snake_positions
        self.max_x = max_size[0] - 1
        self.max_y = max_size[1] - 1
        self.current_food: MapPoint | None = None

    def generate(self) -> None:
        while True:
            food_pos: MapPoint = MapPoint(
                random.randint(0, self.max_x), random.randint(0, self.max_y)
            )

            if all([pos != food_pos for pos in self.snake_positions]):
                self.current_food = food_pos
                return


class Map:
    render: RenderInfo = {"color": Colors.JET_JET_JET}

    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def get_center(self) -> MapPoint:
        return MapPoint(int(self._width / 2) - 1, int(self._height / 2) - 1)

    def is_point_out_of_bounds(self, point: MapPoint) -> bool:
        return (
            point.x < 0
            or point.y < 0
            or point.x >= self._width
            or point.y >= self._height
        )