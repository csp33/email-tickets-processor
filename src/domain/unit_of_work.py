from abc import abstractmethod

from contextlib import contextmanager


class UnitOfWork:
    @contextmanager
    @abstractmethod
    def __call__(self):
        pass

    @abstractmethod
    def flush(self) -> None:
        pass
