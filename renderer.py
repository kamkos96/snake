from colors import Colors, PygameColor
from common import Coordinate, PxSize
from objects import Food, Map, MapPoint, Snake
from window_manager import WindowManager

MAP_POINT_SIZE: PxSize = (8, 8)
SPACE_SIZE: PxSize = (2, 2)


class Renderer:
    def __init__(self, _map: Map, snake: Snake, food: Food):
        self.map = _map
        self.snake = snake
        self.food = food

    @staticmethod
    def _calculate_point_pos(amount: int, size: int, space_size: int) -> int:
        """Function that calculates pixel position in one dimension assuming that
        the start position is 0. It is calculated based on
        amount of rectangles on the way, their size and space between them.
        Can also be used to calculate map size (using maximum amount).

        Args:
            amount (int): amount of rectangles
            size (int): size of rectangle in current dimension
            space_size (int): size of space between rectangles in current dimension

        Returns:
            int: pixel position calculated from 0
        """
        return (amount * size) + (amount + 1) * space_size

    def get_map_size_in_pixels(self) -> Coordinate:
        args = list(zip((self.map.width, self.map.height), MAP_POINT_SIZE, SPACE_SIZE))
        return (
            self._calculate_point_pos(*args[0]),
            self._calculate_point_pos(*args[1]),
        )

    def render_map_points(self, wm: WindowManager, start_anker: Coordinate) -> None:
        x_anker, y_anker = start_anker
        x_size, y_size = MAP_POINT_SIZE
        x_space_size, y_space_size = SPACE_SIZE

        def _calc_start_pos(x_num: int, y_num: int):
            return (
                x_anker + Renderer._calculate_point_pos(x_num, x_size, x_space_size),
                y_anker + Renderer._calculate_point_pos(y_num, y_size, y_space_size),
            )

        def _draw_point_rect(x_num: int, y_num: int, color: PygameColor):
            start_pos = _calc_start_pos(x_num, y_num)
            wm.draw_rectangle(start_pos, x_size, y_size, color)

        wm.draw_background(Colors.JET_BLACK)

        for height_pos in range(self.map._height):
            for width_pos in range(self.map._width):
                _draw_point_rect(width_pos, height_pos, MapPoint.render["color"])

        for point in self.snake.positions:
            _draw_point_rect(*point.coord, Snake.render["color"])

        if self.food.current_food:
            _draw_point_rect(*self.food.current_food.coord, Food.render["color"])

        wm.update_window()
