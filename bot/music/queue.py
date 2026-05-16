import asyncio
import random
from collections import deque

class MusicQueue:
    def __init__(self):
        self._queue = deque()
        self.loop_mode = 0  # 0: None, 1: Track, 2: Queue
        self.history = []
        self.autoplay = False

    def __len__(self):
        return len(self._queue)

    def __iter__(self):
        yield from self._queue

    @property
    def is_empty(self) -> bool:
        return len(self._queue) == 0

    def get_next(self):
        if self.is_empty:
            return None
        return self._queue.popleft()

    def add(self, item):
        self._queue.append(item)

    def add_first(self, item):
        self._queue.appendleft(item)

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(list(self._queue))

    def remove(self, index: int):
        if 0 <= index < len(self._queue):
            del self._queue[index]
            return True
        return False

    def get_queue_list(self):
        return list(self._queue)


