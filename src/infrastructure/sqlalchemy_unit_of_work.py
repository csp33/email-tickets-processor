from contextlib import contextmanager

from sqlalchemy.orm import Session

from src.domain.unit_of_work import UnitOfWork


class SQLAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: Session) -> None:
        self.__session = session

    @contextmanager
    def __call__(self):
        try:
            yield self.__session
            self.__session.commit()
        except Exception:
            self.__session.rollback()
            raise
        finally:
            self.__session.close()

    def flush(self) -> None:
        self.__session.flush()
