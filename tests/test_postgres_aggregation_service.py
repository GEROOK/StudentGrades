import pytest

from src.application.services.aggregation_service import (
    GradeCondition,
    OperatorEnum,
    SortingFieldEnum,
    SortingOptionEnum,
)
from src.domain.entities import PointEnum
from src.infrastructure.services.postgres_aggregation_service import (
    PostgresAggregationService,
)


class DummyConn:

    def __init__(self, fetch_records=None, total=0):
        self.fetch_records = fetch_records or []
        self.total = total
        self.last_query = None

    async def fetch(self, query: str):
        self.last_query = query
        return self.fetch_records

    async def fetchrow(self, query: str):
        self.last_query = query
        if self.total is None:
            return None
        return {"total": self.total}



def make_service(conn=None) -> PostgresAggregationService:
    return PostgresAggregationService(conn)



def test_get_from_part_contains_grades_table():
    svc = make_service()
    part = svc._get_from_part()
    assert "FROM grades" in part
    assert "COUNT(*) FILTER" in part


def test_resolve_grade_condition_various_operators():
    svc = make_service()

    cases = [
        (OperatorEnum.EQUAL, "="),
        (OperatorEnum.GREATER_THAN, ">"),
        (OperatorEnum.LESS_THAN, "<"),
        (OperatorEnum.GREATER_EQUAL, ">="),
        (OperatorEnum.LESS_EQUAL, "<="),
    ]

    for op_enum, symbol in cases:
        cond = GradeCondition(target_grade=PointEnum.GOOD, operator=op_enum, val=42)
        where = svc._resolve_grade_condition(cond)
        assert f"number_of_good {symbol} 42" in where


def test_format_query_includes_order_limit_offset_and_where():
    svc = make_service()
    cond = GradeCondition(target_grade=PointEnum.EXCELLENT, operator=OperatorEnum.LESS_EQUAL, val=1)

    query = svc._format_query(
        limit=5,
        offset=10,
        sorting_field=SortingFieldEnum.GROUP_NUMBER,
        sorting_option=SortingOptionEnum.DESCENDING,
        grade_condition=cond,
    )

    assert "ORDER BY group_number desc" in query
    assert "LIMIT 5 OFFSET 10" in query
    assert "number_of_excellent <= 1" in query


def test_format_query_without_grade_condition():
    svc = make_service()
    query = svc._format_query(limit=1, offset=2)
    expected_filters = len(PointEnum)
    actual_filters = query.count("WHERE points =")
    assert actual_filters == expected_filters
    assert "LIMIT 1 OFFSET 2" in query


@pytest.mark.asyncio
async def test_get_aggregate_students_by_grades_maps_records_and_counts():
    records = [
        {
            "full_name": "Alice",
            "number_of_unsatisfactory": 1,
            "number_of_satisfactory": 2,
            "number_of_good": 0,
            "number_of_excellent": 3,
        }
    ]
    conn = DummyConn(fetch_records=records, total=17)
    svc = make_service(conn)

    result = await svc.get_aggregate_students_by_grades(limit=10, offset=0)

    assert result.total == 17
    assert len(result.result) == 1
    student = result.result[0]
    assert student.student_full_name == "Alice"
    assert student.number_of_excellent == 3


@pytest.mark.asyncio
async def test_count_total_students_returns_zero_when_none():
    conn = DummyConn(fetch_records=[], total=None)
    svc = make_service(conn)

    total = await svc._count_total_students()
    assert total == 0


@pytest.mark.asyncio
async def test_get_aggregate_students_passes_query_to_connection():
    records = []
    conn = DummyConn(fetch_records=records, total=0)
    svc = make_service(conn)

    await svc.get_aggregate_students_by_grades(limit=1, offset=0)
    assert conn.last_query is not None
    assert "SELECT" in conn.last_query
