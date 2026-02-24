import dataclasses
import datetime
import enum


class PointEnum(enum.Enum):
    UNSATISFACTORY = 2
    SATISFACTORY = 3
    GOOD = 4
    EXCELLENT = 5


# Тут можно денормализовать
# - Студентов
# - Группы. Сделав между ними m2m связь
@dataclasses.dataclass
class StudentGrade:
    _id: int | None
    student_full_name: str
    group_number: str
    grade_date: datetime.date
    points: PointEnum

    @property
    def is_persisted(self) -> bool:
        return bool(self._id)
