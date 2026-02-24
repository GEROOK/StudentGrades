import abc
import dataclasses
import enum
from typing import List
from src.domain.entities import PointEnum


class OperatorEnum(enum.Enum):
    EQUAL = "eq"
    LESS_THAN = "lt"
    GREATER_THAN = "gt"
    LESS_EQUAL = "le"
    GREATER_EQUAL = "ge"


class SortingOptionEnum(enum.Enum):
    ASCENDING = "asc"
    DESCENDING = "desc"


class SortingFieldEnum(enum.Enum):
    STUDENT_FULL_NAME = "full_name"  # fix me  student_full_name
    GROUP_NUMBER = "group_number"
    GRADE_DATE = "grade_date"


@dataclasses.dataclass
class GradeCondition:
    target_grade: PointEnum
    operator: OperatorEnum
    val: int


@dataclasses.dataclass
class AggregationResult:
    student_full_name: str
    number_of_unsatisfactory: int
    number_of_satisfactory: int
    number_of_good: int
    number_of_excellent: int


@dataclasses.dataclass
class AggregatedStudents:
    total   : int
    result: List[AggregationResult]


class AbstractAggregationService(abc.ABC):
    @abc.abstractmethod
    def get_aggregate_students_by_grades(
        self,
        limit: int,
        offset: int,
        sorting_field: SortingFieldEnum = SortingFieldEnum.STUDENT_FULL_NAME,
        sorting_option: SortingOptionEnum = SortingOptionEnum.ASCENDING,
        grade_condition: GradeCondition | None = None,
    ) -> AggregatedStudents:
        pass


class AbstractAggregationAsyncService(abc.ABC):
    @abc.abstractmethod
    async def get_aggregate_students_by_grades(
        self,
        limit: int,
        offset: int,
        sorting_field: SortingFieldEnum = SortingFieldEnum.STUDENT_FULL_NAME,
        sorting_option: SortingOptionEnum = SortingOptionEnum.ASCENDING,
        grade_condition: GradeCondition | None = None,
    ) -> AggregatedStudents:
        pass
