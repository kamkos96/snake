import pygame
from pygame.rect import Rect

from colors import Colors, PygameColor
from common import Coordinate


class WindowManager:
    def __init__(self, window_size: Coordinate, window_title: str):
        self._window = pygame.display.set_mode(window_size)

        self.set_window_title(window_title)
        self.set_background_color(Colors.JET_BLACK)

    @property
    def window(self):
        return self._window

    def set_window_title(self, title):
        pygame.display.set_caption(title)

    def draw_rectangle(
        self, start_pos: Coordinate, width: int, height: int, color: PygameColor
    ):
        r = Rect(*start_pos, width, height)
        pygame.draw.rect(self.window, color, r)

    def update_window(self):
        pygame.display.update()

    def draw_background(self, bg_color: PygameColor | None = None):
        if not bg_color:
            bg_color = self.bg_color
        self._window.fill(bg_color)

    def set_background_color(self, color: PygameColor):
        self.bg_color = color
