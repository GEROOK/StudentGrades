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
        self._id = _id
        self.student_full_name = student_full_name
        self.group_number = group_number
        self.grade_date = grade_date
        self.points = points
        #TODO: validate fields

    @property
    def is_persisted(self) -> bool:
        return bool(self._id)
