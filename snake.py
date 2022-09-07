#!/usr/bin/env python3.10

import time
from threading import Thread

import pygame
import pygame.locals

from common import MovementDirection, PxSize
from objects import Food, Map, MapPoint, Snake
from renderer import Renderer
from window_manager import WindowManager

TARGET_FRAMERATE = 60
SNAKE_MOVEMENT_PERIOD_MS = 100


def handle_keyboard(snake: Snake) -> None:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.locals.K_UP:
                    snake.set_direction(MovementDirection.UP)
                case pygame.locals.K_DOWN:
                    snake.set_direction(MovementDirection.DOWN)
                case pygame.locals.K_LEFT:
                    snake.set_direction(MovementDirection.LEFT)
                case pygame.locals.K_RIGHT:
                    snake.set_direction(MovementDirection.RIGHT)


def snake_movement_loop(snake: Snake, map: Map, food: Food) -> None:
    while True:
        next_pos: MapPoint = snake.get_next_position()

        if next_pos in snake.positions:
            print("ERROR - snake collides with itself")
            return

        if map.is_point_out_of_bounds(next_pos):
            next_pos.adjust_to_bounds(map)

        if next_pos == food.position:
            snake.move(next_pos, True)
            food.generate()
        else:
            snake.move(next_pos, False)

        pygame.time.wait(SNAKE_MOVEMENT_PERIOD_MS)


if __name__ == "__main__":
    pygame.init()

    # initialize in-game objects
    game_map: Map = Map(40, 40)
    snake: Snake = Snake(game_map.get_center())
    food: Food = Food(snake.positions, (game_map.width, game_map.height))

    # initialize rendering objects
    renderer = Renderer(game_map, snake, food)

    map_px_size: PxSize = renderer.get_map_size_in_pixels()
    padding: PxSize = (10, 10)
    window_size: PxSize = tuple(
        [px_map + px_pad for px_map, px_pad in zip(map_px_size, padding, strict=True)]
    )

    wm = WindowManager(window_size, "Snake")

    # initialize thread responsible for moving snake
    snake_loop_thread = Thread(target=snake_movement_loop, args=(snake, game_map, food))
    snake_loop_thread.start()

    # initialize clock responsible for updating frames
    frame_clock = pygame.time.Clock()

    # enter game loop
    while True:
        handle_keyboard(snake)

        renderer.render_map_points(wm, (5, 5))

        frame_clock.tick(TARGET_FRAMERATE)
