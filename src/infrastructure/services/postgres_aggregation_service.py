from asyncpg import Connection

from src.application.services.aggregation_service import (
    AbstractAggregationAsyncService,
    AggregationResult,
    AggregatedStudents,
    GradeCondition,
    OperatorEnum,
    SortingFieldEnum,
    SortingOptionEnum,
)
from src.domain.entities import PointEnum
from src.infrastructure.consts import GRADES_TABLE_NAME


class PostgresAggregationService(AbstractAggregationAsyncService):
    def __init__(self, conn: Connection) -> None:
        self._conn = conn

    async def get_aggregate_students_by_grades(
        self,
        limit: int,
        offset: int,
        sorting_field: SortingFieldEnum = SortingFieldEnum.STUDENT_FULL_NAME,
        sorting_option: SortingOptionEnum = SortingOptionEnum.ASCENDING,
        grade_condition: GradeCondition | None = None,
    ) -> AggregatedStudents:
        query = self._format_query(
            limit,
            offset,
            sorting_field,
            sorting_option,
            grade_condition,
        )
        records = await self._conn.fetch(query)
        result = []
        for record in records:
            aggregation_result = AggregationResult(
                student_full_name=record["full_name"],
                number_of_unsatisfactory=record["number_of_unsatisfactory"],
                number_of_satisfactory=record["number_of_satisfactory"],
                number_of_good=record["number_of_good"],
                number_of_excellent=record["number_of_excellent"],
            )
            result.append(aggregation_result)
        return AggregatedStudents(
            total=await self._count_total_students(grade_condition), result=result
        )

    def _get_from_part(self) -> str:
        return f"""
        SELECT
        student_full_name AS full_name,
        COUNT(*) FILTER (WHERE points = 2) AS number_of_unsatisfactory,
        COUNT(*) FILTER (WHERE points = 3) AS number_of_satisfactory,
        COUNT(*) FILTER (WHERE points = 4) AS number_of_good,
        COUNT(*) FILTER (WHERE points = 5) AS number_of_excellent
        FROM {GRADES_TABLE_NAME}
        GROUP BY full_name
        """

    def _format_query(
        self,
        limit: int,
        offset: int,
        sorting_field: SortingFieldEnum = SortingFieldEnum.STUDENT_FULL_NAME,
        sorting_option: SortingOptionEnum = SortingOptionEnum.ASCENDING,
        grade_condition: GradeCondition | None = None,
    ) -> str:
        where_part = ""
        if grade_condition is not None:
            where_part = self._resolve_grade_condition(grade_condition)

        order_part = f"""
        ORDER BY {sorting_field.value} {sorting_option.value}
        LIMIT {limit} OFFSET {offset}
        """
        query = f"""
        SELECT * FROM (
        {self._get_from_part()}
        ) AS aggregated_students
        {where_part}
        {order_part}
        """
        return query

    def _resolve_grade_condition(
        self,
        grade_condition: GradeCondition,
    ) -> str:
        field_map = {
            PointEnum.UNSATISFACTORY: "number_of_unsatisfactory",
            PointEnum.SATISFACTORY: "number_of_satisfactory",
            PointEnum.GOOD: "number_of_good",
            PointEnum.EXCELLENT: "number_of_excellent",
        }
        field_name = field_map[grade_condition.target_grade]
        operator_map = {
            OperatorEnum.EQUAL: "=",
            OperatorEnum.GREATER_THAN: ">",
            OperatorEnum.LESS_THAN: "<",
            OperatorEnum.GREATER_EQUAL: ">=",
            OperatorEnum.LESS_EQUAL: "<=",
        }
        operator_symbol = operator_map[grade_condition.operator]
        return f"WHERE {field_name} {operator_symbol} {grade_condition.val}"

    async def _count_total_students(
        self,
        grade_condition: GradeCondition | None = None,
    ) -> int:
        query = "SELECT COUNT(DISTINCT student_full_name) AS total FROM grades;"
        record = await self._conn.fetchrow(query)
        if record is None:
            return 0
        return record["total"]
