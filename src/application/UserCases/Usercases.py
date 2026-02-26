from src.application.services.aggregation_service import (
    AbstractAggregationAsyncService,
    GradeCondition,
    OperatorEnum,
)
from src.domain.entities import PointEnum


class StudentSearchUseCase:
    def __init__(self, aggregation_service: AbstractAggregationAsyncService) -> None:
        self.aggregation_service = aggregation_service

    async def search_students_with_less_than_5_twos(self, limit: int, offset: int):
        grade_condition = GradeCondition(
            target_grade=PointEnum.UNSATISFACTORY,
            operator=OperatorEnum.LESS_THAN,
            val=5,
        )
        return await self.aggregation_service.get_aggregate_students_by_grades(
            grade_condition=grade_condition, limit=limit, offset=offset
        )

    async def search_students_with_more_than_3_twos(self, limit: int, offset: int):
        grade_condition = GradeCondition(
            target_grade=PointEnum.UNSATISFACTORY,
            operator=OperatorEnum.GREATER_THAN,
            val=3,
        )
        return await self.aggregation_service.get_aggregate_students_by_grades(
            grade_condition=grade_condition, limit=limit, offset=offset
        )
