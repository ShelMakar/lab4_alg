from .errors import EmptyQueueError


class Queue:
    _INITIAL_CAPACITY = 4   # должно быть >= 1, иначе % 0

    def __init__(self):
        self._buf = [None] * self._INITIAL_CAPACITY
        self._head = 0
        self._size = 0

    def add_queue(self, value) -> None:
        if self._size == len(self._buf):
            self._grow()
        tail = (self._head + self._size) % len(self._buf)
        self._buf[tail] = value
        self._size += 1

    def pop_queue(self):
        if self._size == 0:
            raise EmptyQueueError("Удаление из пустой очереди")
        value = self._buf[self._head]
        self._buf[self._head] = None          # не держим лишнюю ссылку
        self._head = (self._head + 1) % len(self._buf)
        self._size -= 1
        return value

    def next(self):
        if self._size == 0:
            raise EmptyQueueError("Невозможно посмотреть следующий элемент в пустой очереди")
        return self._buf[self._head]

    def _grow(self) -> None:
        old, cap = self._buf, len(self._buf)
        new = [None] * (cap * 2)
        for i in range(self._size):
            new[i] = old[(self._head + i) % cap]   # выпрямляем кольцо
        self._buf = new
        self._head = 0

    def __len__(self) -> int:
        return self._size

    def __bool__(self) -> bool:
        return self._size > 0