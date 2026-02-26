import dataclasses

@dataclasses.dataclass
class ImportGradesResponse:
    status: str
    recoreds_loaded: int
    students: int


@dataclasses.dataclass
class StudentSearchResponseItem:
    full_name: str
    total_of_twos: int