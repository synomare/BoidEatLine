import argparse
import asyncio
import pygame

from ..engine import EventBus, TimeManager, MetaCore
from ..scenes.swarm_scene import SwarmScene
from .hud import HUD


async def main(swarm: int = 35, mem: int = 256):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("BoidEatLine")
    clock = pygame.time.Clock()

    bus = EventBus()
    tm = TimeManager(60)
    scene = SwarmScene(
        screen.get_width(), screen.get_height(), bus, swarm_size=swarm, mem_capacity=mem
    )
    observer = MetaCore(bus)
    font = pygame.font.SysFont(None, 24)
    hud = HUD(font)
    running = True
    meta_view = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    meta_view = not meta_view
        dt = await tm.tick()
        await scene.update(dt)
        screen.fill((255, 255, 255))
        scene.draw_epitaphs(screen)
        for b in scene.swarm:
            pygame.draw.circle(screen, (0, 0, 0), b.position, 3)
        if meta_view:
            observer.draw_graph(screen)
        top = observer.get_topk()
        avg_remain = (
            sum(b.death_age - b.age for b in scene.swarm) / len(scene.swarm)
            if scene.swarm
            else 0
        )
        hud.set_lines([
            f"FPS: {clock.get_fps():.1f}",
            f"Population: {len(scene.swarm)}",
            f"Avg Life Left: {avg_remain:.1f}",
            "Centrality:" + ", ".join(f"{c:.2f}" for _, c in top)
        ])
        hud.draw(screen)
        pygame.display.flip()
        clock.tick()

    pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--swarm", type=int, default=35)
    parser.add_argument("--mem", type=int, default=256)
    args = parser.parse_args()
    asyncio.run(main(swarm=args.swarm, mem=args.mem))
