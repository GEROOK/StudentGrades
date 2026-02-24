from collections.abc import Iterable

from asyncpg import Connection

from src.infrastructure.consts import GRADES_TABLE_NAME
from src.application.reposotories.student_grades import (
    AbstractStudentGradeAsyncRepository,
)
from src.domain.entities import StudentGrade


class PosgresStudentGradesAsyncRepository(AbstractStudentGradeAsyncRepository):
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    async def save(self, student_grade: StudentGrade) -> StudentGrade:
        result = await self.save_many([student_grade])
        return result[0]

    async def save_many(
        self, student_grades: Iterable[StudentGrade]
    ) -> list[StudentGrade]:
        query = f"""
            INSERT INTO {GRADES_TABLE_NAME}(
                student_full_name,
                group_number,
                    grade_date,
                    points
                ) SELECT x.student_full_name, x.group_number, x.grade_date, x.points
                FROM UNNEST($1::text[], $2::text[], $3::date[], $4::int[]) AS x(student_full_name, group_number, grade_date, points)
                RETURNING id;
            """
        student_full_names = [sg.student_full_name for sg in student_grades]
        group_numbers = [sg.group_number for sg in student_grades]
        grade_dates = [sg.grade_date for sg in student_grades]
        points = [sg.points.value for sg in student_grades]

        records = await self._connection.fetch(
            query,
            student_full_names,
            group_numbers,
            grade_dates,
            points,
        )
        for sg, record in zip(student_grades, records):
            sg._id = record["id"]
        return list(student_grades)
