import io

import pytest

from src.infrastructure.services.importing_csv_service import CSVProvider, ImportingService
from src.domain.entities import PointEnum


class DummyRepo:
    def __init__(self):
        self.saved = []

    async def save(self, student_grade):
        self.saved.append(student_grade)


def test_csvprovider_parses_rows_and_closes_file():
    text = (
        "ФИО;Номер группы;Дата;Оценка\n"
        "Иван Иванов;101;01.01.2020;5\n"
        "Анна Смирнова;102;02.02.2021;4\n"
    )
    raw = text.encode("utf-8")
    provider = CSVProvider(io.BytesIO(raw))

    first = next(provider)
    assert first.student_full_name == "Иван Иванов"
    assert first.group_number == "101"
    assert first.points == PointEnum.EXCELLENT

    second = next(provider)
    assert second.student_full_name == "Анна Смирнова"
    assert second.points == PointEnum.GOOD

    with pytest.raises(StopIteration):
        next(provider)

    provider.__del__()
    assert provider.file.closed


@pytest.mark.asyncio
async def test_importing_service_counts_correctly_and_saves_records():
    csv_text = (
        "ФИО;Номер группы;Дата;Оценка\n"
        "А;1;01.01.2020;2\n"
        "А;1;02.01.2020;3\n"
        "Б;2;03.01.2020;4\n"
    )
    provider = CSVProvider(io.BytesIO(csv_text.encode("utf-8")))

    repo = DummyRepo()
    svc = ImportingService(repo)

    total_rows, unique_students = await svc.import_student_grades(provider)

    assert total_rows == 3
    assert unique_students == 2
    assert len(repo.saved) == 3

    names = [r.student_full_name for r in repo.saved]
    assert names == ["А", "А", "Б"]

