from fastapi import APIRouter, Depends, File, UploadFile, Query
from src.application.UserCases.Usercases import StudentSearchUseCase
from src.application.services.importing_service import AbstractImportingAsyncService
from src.infrastructure.services.postgres_aggregation_service import (
    PostgresAggregationService,
)
from src.interfaces.http.dependencies.services import (
    get_csv_provider,
    get_importing_service,
)
from src.interfaces.http.dependencies.database import get_connection
from asyncpg import Connection

router = APIRouter()


def get_aggregation_service(connection: Connection = Depends(get_connection)):
    return PostgresAggregationService(connection)


def get_student_search_usecase(
    aggregation_service: PostgresAggregationService = Depends(get_aggregation_service),
):
    return StudentSearchUseCase(aggregation_service)


@router.post("/import")
async def import_grades(
    file: UploadFile = File(...),
    importing_service: AbstractImportingAsyncService = Depends(get_importing_service),
):
    provider = await get_csv_provider(file)
    # call the method on the injected service instance
    records_loaded, student_count = await importing_service.import_student_grades(provider)
    return {
        "status": "ok",
        "records_loaded": records_loaded,
        "students": student_count,
    }


@router.get("/students/less-than-5-twos")
async def students_with_less_than_5_twos(
    usecase: StudentSearchUseCase = Depends(get_student_search_usecase),
    limit: int = Query(10, ge=1, include_in_schema=False),
    offset: int = Query(0, ge=0, include_in_schema=False),
):
    aggregated = await usecase.search_students_with_less_than_5_twos(
        limit=limit, offset=offset
    )
    return {
        "results": [
            {
                "full_name": student.student_full_name,
                "total_of_twos": student.number_of_unsatisfactory,
            }
            for student in aggregated.result
        ],
    }


@router.get("/students/more-than-3-twos")
async def students_with_more_than_3_twos(
    usecase: StudentSearchUseCase = Depends(get_student_search_usecase),
    limit: int = Query(10, ge=1, include_in_schema=False),
    offset: int = Query(0, ge=0, include_in_schema=False),
):
    aggregated = await usecase.search_students_with_more_than_3_twos(
        limit=limit, offset=offset
    )
    # `aggregated` is an `AggregatedStudents` dataclass; access its fields
    return {
        "results": [
            {
                "full_name": student.student_full_name,
                "total_of_twos": student.number_of_unsatisfactory,
            }
            for student in aggregated.result
        ],
    }
