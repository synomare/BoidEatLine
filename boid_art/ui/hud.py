import pygame
from typing import List, Tuple


class HUD:
    def __init__(self, font: pygame.font.Font, pos: Tuple[int, int] = (10, 10)):
        self.font = font
        self.pos = pos
        self.lines: List[str] = []

    def set_lines(self, lines: List[str]):
        self.lines = lines

    def draw(self, surface: pygame.Surface):
        x, y = self.pos
        for line in self.lines:
            img = self.font.render(line, True, (0, 0, 0))
            surface.blit(img, (x, y))
            y += img.get_height() + 2
