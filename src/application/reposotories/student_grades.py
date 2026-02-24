import abc
from collections.abc import Iterable
from typing import List
from src.domain.entities import StudentGrade


class AbstractStudentGradeRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, student_grade: StudentGrade) -> StudentGrade:
        pass

    @abc.abstractmethod
    def save_many(self, student_grades: Iterable[StudentGrade]) -> List[StudentGrade]:
        pass


class AbstractStudentGradeAsyncRepository(abc.ABC):
    @abc.abstractmethod
    async def save(self, student_grade: StudentGrade) -> StudentGrade:
        pass

    @abc.abstractmethod
    async def save_many(
        self, student_grades: Iterable[StudentGrade]
    ) -> List[StudentGrade]:
        pass
