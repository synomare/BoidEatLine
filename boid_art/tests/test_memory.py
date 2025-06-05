from pygame.math import Vector2

from boid_art.engine.memory import SubjectiveStream


def test_stream_compress():
    stream = SubjectiveStream(capacity=10, compress_ratio=0.5)
    for i in range(20):
        stream.append(Vector2(i, i))
    assert len(stream.data) <= 5
