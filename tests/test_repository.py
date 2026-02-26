import pytest

from src.infrastructure.repositories.student_grades.postgres import (
    PosgresStudentGradesAsyncRepository,
)
from src.domain.entities import StudentGrade, PointEnum


class DummyConn:
    def __init__(self):
        self.last_query = None
        self.args = None

    async def fetch(self, query, *args):
        self.last_query = query
        self.args = args
        # pretend IDs are returned sequentially
        return [{"id": i + 1} for i, _ in enumerate(args[0])]


@pytest.mark.asyncio
async def test_save_many_assigns_ids_and_builds_query():
    conn = DummyConn()
    repo = PosgresStudentGradesAsyncRepository(conn)

    grades = [
        StudentGrade(_id=None, student_full_name="A", group_number="1", grade_date="2020-01-01", points=PointEnum.GOOD),
        StudentGrade(_id=None, student_full_name="B", group_number="2", grade_date="2020-02-02", points=PointEnum.EXCELLENT),
    ]

    result = await repo.save_many(grades)
    # ids should be filled
    assert grades[0]._id == 1
    assert grades[1]._id == 2
    assert result == grades

    assert "INSERT INTO" in conn.last_query
    # arguments should contain parallel lists
    assert len(conn.args) == 4
    assert conn.args[0] == ["A", "B"]
    assert conn.args[3] == [PointEnum.GOOD.value, PointEnum.EXCELLENT.value]


@pytest.mark.asyncio
async def test_save_delegates_to_save_many():
    conn = DummyConn()
    repo = PosgresStudentGradesAsyncRepository(conn)
    grade = StudentGrade(_id=None, student_full_name="C", group_number="3", grade_date="2020-03-03", points=PointEnum.SATISFACTORY)
    saved = await repo.save(grade)
    assert saved is grade
    assert grade._id == 1
