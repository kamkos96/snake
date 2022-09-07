from enum import Enum

from pygame.color import Color as PygameColor


class Colors(PygameColor, Enum):
    def __hash__(self):
        return sum(
            value * multiplier
            for value, multiplier in [
                (self.r, 0x10000),
                (self.g, 0x100),
                (self.b, 0x1),
            ]
        )

    BLACK = PygameColor(0x00, 0x00, 0x00)
    JET_BLACK = PygameColor(0x0A, 0x0A, 0x0A)
    JET_JET_JET = PygameColor(0x0C, 0x0C, 0x0C)
    DARK_GRAY = PygameColor(0x21, 0x21, 0x21)
    GUNMETAL_GRAY = PygameColor(0x4E, 0x54, 0x5C)
    GRAY = PygameColor(0xEF, 0xEF, 0xEF)
    WHITE = PygameColor(0xFF, 0xFF, 0xFF)
    RED = PygameColor(0xFF, 0x00, 0x00)
    GREEN = PygameColor(0x00, 0xFF, 0x00)
    BLUE = PygameColor(0x00, 0x00, 0xFF)
    YELLOW = PygameColor(0xFF, 0xFF, 0x00)
    CYAN = PygameColor(0x00, 0xFF, 0xFF)
    MAGENTA = PygameColor(0xFF, 0x00, 0xFF)
