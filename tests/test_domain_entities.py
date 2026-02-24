from datetime import date

from src.domain.entities import PointEnum, StudentGrade


def test_point_enum_values():
    assert PointEnum.UNSATISFACTORY.value == 2
    assert PointEnum.EXCELLENT.value == 5


def test_studentgrade_is_persisted_property():
    sg = StudentGrade(_id=None, student_full_name="X", group_number="1", grade_date=date.today(), points=PointEnum.GOOD)
    assert not sg.is_persisted
    sg2 = StudentGrade(_id=123, student_full_name="Y", group_number="2", grade_date=date.today(), points=PointEnum.SATISFACTORY)
    assert sg2.is_persisted
