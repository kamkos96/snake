#!/usr/bin/env python3

import time

import pygame

from common import PxSize
from objects import Food, Map, MapPoint, Snake
from renderer import Renderer
from window_manager import WindowManager

TARGET_FRAMERATE = 60
SNAKE_MOVEMENT_PERIOD_MS = 250


def move_snake(snake: Snake, map: Map, food: Food):
    next_pos: MapPoint = snake.get_next_position()

    if next_pos in snake.positions:
        print("ERROR - snake collides with itself")

    if map.is_point_out_of_bounds(next_pos):
        next_pos.adjust_to_bounds(map)
        # print("ERROR - next snake position out of map")

    if next_pos == food.current_food:
        snake.move(next_pos, True)
        food.generate()
    else:
        snake.move(next_pos, False)


if __name__ == "__main__":
    pygame.init()

    # initialize in-game objects
    game_map: Map = Map(40, 40)
    snake: Snake = Snake(game_map.get_center())
    food: Food = Food(snake.positions, (game_map.width, game_map.height))
    food.generate()

    # initialize rendering objects
    renderer = Renderer(game_map, snake, food)

    (map_width, map_height) = renderer.get_map_size_in_pixels()
    padding: PxSize = (10, 10)

    wm = WindowManager((map_width + padding[0], map_height + padding[1]), "Snake")

    # initialize game loop variables
    frame_num = 0
    snake_movement_timer = time.time_ns()

    # enter game loop
    while True:
        start_time = time.time_ns()

        if time.time_ns() - snake_movement_timer >= SNAKE_MOVEMENT_PERIOD_MS * 1000000:
            move_snake(snake, game_map, food)
            snake_movement_timer = time.time_ns()

        renderer.render_map_points(wm, (5, 5))

        frame_num += 1

        end_time = time.time_ns()
        sleep_ms: int = int((1000 / TARGET_FRAMERATE) - (end_time - start_time) / 1000000)

        if sleep_ms > 0:
            pygame.time.delay(sleep_ms)
