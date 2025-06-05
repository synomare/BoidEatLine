from collections import deque
from typing import List
from pygame.math import Vector2
import numpy as np


class SubjectiveStream:
    def __init__(self, capacity: int = 256, compress_ratio: float = 0.5):
        self.capacity = capacity
        self.compress_ratio = compress_ratio
        self.data: deque[Vector2] = deque(maxlen=capacity)

    def append(self, p: Vector2):
        self.data.append(Vector2(p))
        if len(self.data) >= self.capacity:
            self.compress()

    def flush(self) -> List[Vector2]:
        out = list(self.data)
        self.data.clear()
        return out

    def compress(self):
        if not self.data:
            return
        max_points = int(self.capacity * self.compress_ratio)
        if len(self.data) <= max_points:
            return
        pts = np.array([[p.x, p.y] for p in self.data])
        # Douglas-Peucker simplification
        simplified_idx = douglas_peucker(pts, max_points)
        self.data = deque([Vector2(*pts[i]) for i in simplified_idx], maxlen=self.capacity)


def douglas_peucker(points: np.ndarray, max_points: int) -> List[int]:
    if len(points) <= 2 or len(points) <= max_points or max_points < 2:
        return list(range(len(points)))

    # Iterative DP using stack
    stack = [(0, len(points) - 1)]
    keep = {0, len(points) - 1}
    while stack and len(keep) < max_points:
        start, end = stack.pop()
        line = points[end] - points[start]
        line_norm = line / np.linalg.norm(line) if np.linalg.norm(line) else line
        indices = range(start + 1, end)
        if not indices:
            continue
        vecs = points[start + 1 : end] - points[start]
        dists = np.abs(np.cross(line_norm, vecs))
        idx_rel = int(np.argmax(dists))
        idx = start + 1 + idx_rel
        keep.add(idx)
        if len(keep) >= max_points:
            break
        stack.append((idx, end))
        stack.append((start, idx))

    result = sorted(keep)
    return result
