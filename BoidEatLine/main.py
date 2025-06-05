import pygame
from SceneClass import SwarmScene


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("BoidEatLine")
    clock = pygame.time.Clock()
    scene = SwarmScene(screen.get_width(), screen.get_height())

    running = True
    mouse_down = False
    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
                scene.touch_began(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
                scene.touch_ended(event.pos)
            elif event.type == pygame.MOUSEMOTION and mouse_down:
                scene.touch_moved(event.pos)

        scene.update(dt)
        scene.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
