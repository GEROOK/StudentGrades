# StudentGrade

REST-сервис на FastAPI для управления оценками студентов.

## Требования

- Python 3.12+
- Poetry
- Docker & Docker Compose

## Запуск

### Вариант 1: В Docker Compose (рекомендуется)

```bash
docker compose up -d
```

Это запустит приложение и PostgreSQL в контейнерах. Приложение будет доступно на `http://localhost:8000`

Остановка:
```bash
docker compose down
```

### Вариант 2: Локальный запуск

#### 1. Установка зависимостей

```bash
poetry install
```

#### 2. Запуск базы данных

```bash
docker compose up -d db
```

#### 3. Запуск приложения

```bash
poetry run python -m uvicorn src.interfaces.http.main:app --reload
```

Приложение доступно на `http://localhost:8000`

## Проверка API

### Интерактивная документация (Swagger UI)

Откройте в браузере: **http://localhost:8000/docs**

Здесь можно протестировать все endpoints прямо из браузера.

### Полезные команды Docker

**Просмотр логов приложения:**
```bash
docker compose logs app -f
```

**Просмотр статуса контейнеров:**
```bash
docker compose ps
```

**Пересборка образа после изменений:**
```bash
docker compose build
docker compose up -d
```

**Выполнение команд в контейнере:**
```bash
docker compose exec app pytest
docker compose exec app bash
```

### Примеры запросов (curl)

**Импорт данных из CSV:**
```bash
curl -X POST "http://localhost:8000/import" \
  -F "file=@grades.csv"
```

**Студенты с менее чем 5 двойками:**
```bash
curl "http://localhost:8000/students/less-than-5-twos?limit=10"
```

**Студенты с более чем 3 двойками:**
```bash
curl "http://localhost:8000/students/more-than-3-twos?limit=10"
```

## Тестирование

### Запуск всех тестов

```bash
pytest
```

### Запуск конкретного файла тестов

```bash
pytest tests/test_importing_service.py -v
pytest tests/test_routes.py -v
pytest tests/test_domain_entities.py -v
pytest tests/test_postgres_aggregation_service.py -v
```

### Запуск с покрытием кода

```bash
pytest --cov=src --cov-report=html
```

## Формат CSV для импорта

```
ФИО;Номер группы;Дата;Оценка
Иван Иванов;101;01.01.2020;5
Анна Смирнова;102;02.02.2021;4
Петр Петров;103;15.03.2021;2
```

**Требования:**
- Разделитель: `;` (точка с запятой)
- Кодировка: UTF-8
- Дата: DD.MM.YYYY
- Оценка: 2, 3, 4 или 5
