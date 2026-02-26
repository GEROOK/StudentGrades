from fastapi import Depends, UploadFile
from src.infrastructure.services.importing_csv_service import CSVProvider
from src.infrastructure.services.importing_csv_service import ImportingService
from .repositories import  get_student_grade_repository


async def get_csv_provider(file: UploadFile) -> CSVProvider:
    return CSVProvider(file.file)


async def get_importing_service(
    student_grade_repository=Depends(get_student_grade_repository)
) -> ImportingService:
    return ImportingService(student_grade_repository)
