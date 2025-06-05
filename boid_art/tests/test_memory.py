from pygame.math import Vector2

from boid_art.engine.memory import SubjectiveStream


def test_stream_compress():
    stream = SubjectiveStream(capacity=10, compress_ratio=0.5)
    for i in range(20):
        stream.append(Vector2(i, i))
    assert len(stream.data) <= 5


def test_compress_no_recursion():
    stream = SubjectiveStream(capacity=5, compress_ratio=0.2)
    for i in range(5):
        stream.append(Vector2(i, 0))
    # ratio so low that max_points < 2
    stream.compress()
    assert len(stream.data) <= 5
