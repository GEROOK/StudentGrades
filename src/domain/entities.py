import dataclasses
import datetime
import enum


class PointEnum(enum.Enum):
    UNSATISFACTORY = 2
    SATISFACTORY = 3
    GOOD = 4
    EXCELLENT = 5


@dataclasses.dataclass(init = False)
class StudentGrade:
    _id: int | None
    student_full_name: str
    group_number: str
    grade_date: datetime.date
    points: PointEnum

    def __init__(
        self,
        _id: int | None,
        student_full_name: str,
        group_number: str,
        grade_date: datetime.date,
        points: PointEnum,
    ) -> None:
        self._validate_fields(student_full_name, group_number, grade_date)
        self._id = _id
        self.student_full_name = student_full_name
        self.group_number = group_number
        self.grade_date = grade_date
        self.points = points

    def _validate_fields(
        self,
        student_full_name: str,
        group_number: str,
        grade_date: datetime.date,
    ) -> None:
        if not student_full_name or not student_full_name.strip():
            raise ValueError("student_full_name cannot be empty")
        if not group_number or not group_number.strip():
            raise ValueError("group_number cannot be empty")
        if grade_date > datetime.date.today():
            raise ValueError("grade_date cannot be in the future")

    @property
    def is_persisted(self) -> bool:
        return bool(self._id)
