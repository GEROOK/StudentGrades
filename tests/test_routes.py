import io

import pytest
from fastapi.testclient import TestClient

from src.interfaces.http.main import get_app


@pytest.fixture

def client():
    app = get_app()
    with TestClient(app) as c:
        yield c


def make_csv_bytes(text: str) -> bytes:
    return text.encode("utf-8")


def test_import_endpoint_success(client):
    csv = (
        "ФИО;Номер группы;Дата;Оценка\n"
        "Иван Иванов;101;01.01.2020;5\n"
        "Анна Смирнова;102;02.02.2021;4\n"
    )
    response = client.post("/import", files={"file": ("grades.csv", make_csv_bytes(csv), "text/csv")})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["recoreds_loaded"] == 2
    assert data["students"] == 2


def test_import_endpoint_invalid_data_returns_bad_request(client):

    bad_csv = "ФИО;Номер группы;Дата\nА;1;01.01.2020\n"
    response = client.post("/import", files={"file": ("bad.csv", make_csv_bytes(bad_csv), "text/csv")})
    assert response.status_code == 400
    # detail should mention missing required columns
    assert "Missing required columns" in response.json().get("detail", "")

    # invalid grade value
    bad_csv2 = (
        "ФИО;Номер группы;Дата;Оценка\n"
        "А;1;01.01.2020;invalid\n"
    )
    response2 = client.post("/import", files={"file": ("bad2.csv", make_csv_bytes(bad_csv2), "text/csv")})
    assert response2.status_code == 400
    assert "Invalid grade value" in response2.json().get("detail", "")
