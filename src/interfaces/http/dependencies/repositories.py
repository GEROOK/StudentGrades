from src.infrastructure.repositories.student_grades.postgres import PosgresStudentGradesAsyncRepository
from .database import  get_connection
from fastapi import Depends
from typing import Annotated

def get_student_grade_repository(connection=Depends(get_connection)) -> PosgresStudentGradesAsyncRepository:
    return PosgresStudentGradesAsyncRepository(connection)
    

StudentGradeRepositoryDep = Annotated[PosgresStudentGradesAsyncRepository, Depends(get_student_grade_repository)]
