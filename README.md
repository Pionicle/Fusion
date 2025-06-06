# Fusion

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-blue.svg)
![Pydantic](https://img.shields.io/badge/Pydantic-2.11-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17.2-blue.svg)
![Redis](https://img.shields.io/badge/Redis-8.0-blue.svg)

## Технологии

- **PostgreSQL**: Реляционная база данных.
- **Redis**: База данных для хранения кэша.
- **Python**:
  - **FastAPI**: Веб-фреймворк для создания API.
  - **SQLAlchemy**: ORM для работы с БД.
  - **Pydantic**: Валидатор для проверки данных.

---


## Запуск

1. Установите зависимости:
```sh
cd Fusion
poetry install
```

2. Соберите docker-compose файл:
```sh
docker-compose up -d
```

3. Заполните базу данных:
```sh
cd sql && poetry run python fill_data.py && cd ..
```

3. Запустите приложение:
```sh
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

4. Откройте браузер и перейдите по адресу: [http://localhost:8000/docs#](http://localhost:8000/docs#)
