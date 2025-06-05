import asyncio
import time
from collections import defaultdict
from typing import Callable, Dict, List


class EventBus:
    """Simple asynchronous publish-subscribe bus."""

    def __init__(self) -> None:
        self._subs: Dict[str, List[Callable]] = defaultdict(list)

    def emit(self, topic: str, **payload):
        handlers = list(self._subs.get(topic, []))
        for h in handlers:
            coro = h(**payload)
            if asyncio.iscoroutine(coro):
                asyncio.create_task(coro)

    def on(self, topic: str):
        def _decor(fn: Callable):
            self._subs[topic].append(fn)
            return fn
        return _decor


class TimeManager:
    def __init__(self, fps: int = 60):
        self.fps = fps
        self._last = time.perf_counter()

    async def tick(self) -> float:
        now = time.perf_counter()
        dt = now - self._last
        sleep_time = max(0, 1.0 / self.fps - dt)
        if sleep_time:
            await asyncio.sleep(sleep_time)
            now = time.perf_counter()
            dt = now - self._last
        self._last = now
        return dt
