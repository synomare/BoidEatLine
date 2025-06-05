"""Utilities for running pygame in headless mode for tests."""
import os

if os.environ.get("SDL_VIDEODRIVER") == "dummy":
    import pygame

    pygame.display.init = lambda *a, **k: None
    pygame.display.set_mode = lambda *a, **k: None
