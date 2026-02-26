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
        self._validate_columns()

    def _validate_columns(self):
        required_columns = {"ФИО", "Номер группы", "Дата", "Оценка"}
        if not self.reader.fieldnames:
            raise ValueError("CSV file is empty")
        missing_columns = required_columns - set(self.reader.fieldnames)
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

    def __iter__(self):
        return self

    def __next__(self):
        try:
            row = next(self.reader)
            student_grade = StudentGrade(
                _id=None,
                student_full_name=self._validate_string(row["ФИО"]),
                group_number=self._validate_string(row["Номер группы"]),
                grade_date=self._validate_date(row["Дата"]),
                points=self._validate_points(row["Оценка"]),
            )
            return student_grade
        except StopIteration:
            raise

    def _validate_string(self, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("String value cannot be empty")
        return value.strip()

    def _validate_date(self, value: str) -> datetime.date:
        try:
            return datetime.datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError(f"Invalid date format: {value}")

    def _validate_points(self, value: str) -> PointEnum:
        try:
            return PointEnum(int(value))
        except (ValueError, KeyError):
            raise ValueError(f"Invalid grade value: {value}")

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
