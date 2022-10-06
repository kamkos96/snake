import random

from common import Colors, Coordinate, MovementDirection, RenderInfo


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


class Segment(MapPoint):
    def __init__(self, x: int, y: int, color: Colors):
        MapPoint.__init__(self, x, y)
        self.color = color


class Snake:
    head_color: Colors = Colors.RED
    body_color: Colors = Colors.WHITE
    extend_color: Colors = Colors.YELLOW

    def __init__(self, initial_placement: MapPoint) -> None:
        x = initial_placement.x
        y = initial_placement.y

        self.positions: list[Segment] = [
            Segment(x, y, self.head_color),
            Segment(x, y + 1, self.body_color),
            Segment(x, y + 2, self.body_color),
        ]
        self.current_dir: MovementDirection = MovementDirection.UP
        self.next_dir: MovementDirection | None = None
        self.moved_after_direction_change: bool = False

    def __len__(self) -> int:
        return len(self.positions)

    @property
    def size(self) -> int:
        return len(self)

    def set_direction(self, direction: MovementDirection) -> None:
        if direction in (self.current_dir, self.current_dir * -1):
            print("Cannot change direction to forwards or backwards")
            return

        if not self.moved_after_direction_change:
            self.next_dir = direction
            return

        self.current_dir = direction
        self.moved_after_direction_change = False

    def get_next_position(self) -> MapPoint:
        base: MapPoint = self.positions[0]
        match self.current_dir:
            case MovementDirection.UP:
                return MapPoint(base.x, base.y - 1)
            case MovementDirection.DOWN:
                return MapPoint(base.x, base.y + 1)
            case MovementDirection.LEFT:
                return MapPoint(base.x - 1, base.y)
            case MovementDirection.RIGHT:
                return MapPoint(base.x + 1, base.y)

    def move(self, next_pos: MapPoint, currently_eating: bool = False) -> None:
        if self.positions[0].color == self.head_color:
            self.positions[0].color = self.body_color

        self.positions.insert(
            0,
            Segment(
                next_pos.x,
                next_pos.y,
                self.extend_color if currently_eating else self.head_color,
            ),
        )

        if not currently_eating:
            self.positions.pop()

        self.moved_after_direction_change = True

        if self.next_dir:
            self.current_dir = self.next_dir
            self.next_dir = None
            self.moved_after_direction_change = False

    def move_and_eat(self, next_pos: MapPoint) -> None:
        self.move(next_pos, True)


class Food:
    render: RenderInfo = {"color": Colors.GREEN}

    def __init__(self, snake_positions: list[MapPoint], max_size: Coordinate) -> None:
        self.snake_positions: list[MapPoint] = snake_positions
        self.max_x = max_size[0] - 1
        self.max_y = max_size[1] - 1
        self.position: MapPoint | None = None
        self.generate()

    def generate(self) -> None:
        while True:
            food_pos: MapPoint = MapPoint(
                random.randint(0, self.max_x), random.randint(0, self.max_y)
            )

            if all([snake_pos != food_pos for snake_pos in self.snake_positions]):
                self.position = food_pos
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
