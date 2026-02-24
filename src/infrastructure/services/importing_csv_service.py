import datetime
import io
from typing import BinaryIO
from src.application.services.importing_service import (
    AbstractImportingAsyncService,
    AbstractProvider,
)
from src.domain.entities import PointEnum, StudentGrade
from src.application.reposotories.student_grades import (
    AbstractStudentGradeAsyncRepository,
)

import csv


class CSVProvider(AbstractProvider):
    def __init__(self, file_io: BinaryIO):
        self.file = io.TextIOWrapper(file_io, encoding="utf-8-sig")
        self.reader = csv.DictReader(self.file, delimiter=";")

    def __iter__(self):
        return self

    def __next__(self):
        try:
            row = next(self.reader)
            student_grade = StudentGrade(
                _id=None,
                student_full_name=row["ФИО"],
                group_number=row["Номер группы"],
                grade_date=datetime.datetime.strptime(row["Дата"], "%d.%m.%Y").date(),
                points=PointEnum(int(row["Оценка"])),
            )
            return student_grade
        except StopIteration:
            raise

    def __del__(self):
        if not self.file.closed:
            self.file.close()


class ImportingService(AbstractImportingAsyncService):
    def __init__(self, grades_repository: AbstractStudentGradeAsyncRepository) -> None:
        self._grades_repository = grades_repository

    async def import_student_grades(self, provider: AbstractProvider) -> tuple[int,int]:
        count = 0
        student_count = 0
        student_names = set()
        for studentgrade in provider:
            await self._grades_repository.save(studentgrade)
            count += 1
            if studentgrade.student_full_name not in student_names:
                student_names.add(studentgrade.student_full_name)
                student_count += 1
        return count, student_count
