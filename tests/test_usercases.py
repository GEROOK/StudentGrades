import pytest

from src.application.Usercases.Usercases import StudentSearchUseCase
from src.application.services.aggregation_service import GradeCondition
from src.domain.entities import PointEnum
from src.application.services.aggregation_service import OperatorEnum


class DummyAggService:
    def __init__(self):
        self.called_with = None
        self.return_value = None

    async def get_aggregate_students_by_grades(
        self, *, limit, offset, grade_condition=None, **kwargs
    ):
        self.called_with = {
            "limit": limit,
            "offset": offset,
            "grade_condition": grade_condition,
        }
        return self.return_value


@pytest.mark.asyncio
async def test_search_students_with_less_than_5_twos():
    dummy = DummyAggService()
    dummy.return_value = "ok1"
    usecase = StudentSearchUseCase(dummy)
    result = await usecase.search_students_with_less_than_5_twos(limit=3, offset=7)

    assert result == "ok1"
    assert dummy.called_with["limit"] == 3
    assert dummy.called_with["offset"] == 7
    cond = dummy.called_with["grade_condition"]
    assert isinstance(cond, GradeCondition)
    assert cond.target_grade == PointEnum.UNSATISFACTORY
    assert cond.operator == OperatorEnum.LESS_THAN
    assert cond.val == 5


@pytest.mark.asyncio
async def test_search_students_with_more_than_3_twos():
    dummy = DummyAggService()
    dummy.return_value = "ok2"
    usecase = StudentSearchUseCase(dummy)
    result = await usecase.search_students_with_more_than_3_twos(limit=1, offset=2)

    assert result == "ok2"
    cond = dummy.called_with["grade_condition"]
    assert cond.target_grade == PointEnum.UNSATISFACTORY
    assert cond.operator == OperatorEnum.GREATER_THAN
    assert cond.val == 3
