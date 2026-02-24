import abc
from builtins import int
from src.domain.entities import StudentGrade


class AbstractProvider(abc.ABC):
    @abc.abstractmethod
    def __iter__(self):
        pass

    @abc.abstractmethod
    def __next__(self) -> StudentGrade:
        pass


class AbstractImportingService(abc.ABC):
    @abc.abstractmethod
    def import_student_grades(
        self,
        provider: AbstractProvider,
    ) -> int:
        """
        Импортирует оценки студентов из провайдера. Возвращает количество импортированных записей.
        """
        pass


class AbstractImportingAsyncService(abc.ABC):
    @abc.abstractmethod
    async def import_student_grades(
        self,
        provider: AbstractProvider,
    ) -> tuple[int, int]:
        """
        Импортирует оценки студентов из провайдера. Возвращает количество импортированных записей и количество студентов.
        """
        pass
