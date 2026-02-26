from datetime import date
import datetime
import pytest

from src.domain.entities import PointEnum, StudentGrade


def test_point_enum_values():
    assert PointEnum.UNSATISFACTORY.value == 2
    assert PointEnum.EXCELLENT.value == 5


def test_studentgrade_is_persisted_property():
    sg = StudentGrade(_id=None, student_full_name="X", group_number="1", grade_date=date.today(), points=PointEnum.GOOD)
    assert not sg.is_persisted
    sg2 = StudentGrade(_id=123, student_full_name="Y", group_number="2", grade_date=date.today(), points=PointEnum.SATISFACTORY)
    assert sg2.is_persisted


def test_studentgrade_field_validations():
    with pytest.raises(ValueError) as e1:
        StudentGrade(_id=None, student_full_name="", group_number="1", grade_date=date.today(), points=PointEnum.GOOD)
    assert "student_full_name" in str(e1.value)

    with pytest.raises(ValueError) as e2:
        StudentGrade(_id=None, student_full_name="A", group_number="", grade_date=date.today(), points=PointEnum.GOOD)
    assert "group_number" in str(e2.value)


def test_future_date_allowed():
    future = date.today() + datetime.timedelta(days=7)
    sg = StudentGrade(_id=None, student_full_name="A", group_number="1", grade_date=future, points=PointEnum.GOOD)
    assert sg.grade_date == future
