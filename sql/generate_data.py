import csv
from faker import Faker
import random
from datetime import datetime

# Инициализация Faker для генерации реалистичных данных
fake = Faker()

# Определение значений для ENUM
NATIONALITIES = ["Russian", "American", "British", "French", "German"]
BOOK_CATEGORIES = ["Fiction", "Non-fiction", "Science", "History", "Fantasy"]

# Количество записей для генерации
NUM_AUTHORS = 50
NUM_BOOKS = 100
NUM_READERS = 100
NUM_BOOK_READERS = 300

# Генерация данных для таблицы authors
authors = []
author_ids = list(range(1, NUM_AUTHORS + 1))
for i in range(1, NUM_AUTHORS + 1):
    authors.append(
        {
            "author_id": i,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "nationality": random.choice(NATIONALITIES),
        }
    )

# Генерация данных для таблицы books
books = []
book_titles = set()  # Для обеспечения уникальности заголовков
for i in range(1, NUM_BOOKS + 1):
    while True:
        title = fake.catch_phrase()[:50]  # Ограничиваем длину до 50 символов
        if title not in book_titles and title:  # Проверяем уникальность и непустоту
            book_titles.add(title)
            break
    publication_year = fake.date_between(
        start_date=datetime(1800, 1, 1), end_date=datetime(2025, 12, 31)
    )
    books.append(
        {
            "book_id": i,
            "title": title,
            "publication_year": publication_year.strftime("%Y-%m-%d"),
            "category": random.choice(BOOK_CATEGORIES),
            "author_id": random.choice(author_ids)
            if random.random() > 0.1
            else None,  # 10% книг без автора
        }
    )

# Генерация данных для таблицы readers
readers = []
reader_emails = set()  # Для обеспечения уникальности email
for i in range(1, NUM_READERS + 1):
    while True:
        email = fake.email()[:255]  # Ограничиваем длину до 255 символов
        if email not in reader_emails:
            reader_emails.add(email)
            break
    readers.append(
        {
            "reader_id": i,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": email,
        }
    )

# Генерация данных для таблицы book_readers
book_readers = []
book_reader_pairs = set()  # Для обеспечения уникальности пар (book_id, reader_id)
for _ in range(NUM_BOOK_READERS):
    while True:
        book_id = random.randint(1, NUM_BOOKS)
        reader_id = random.randint(1, NUM_READERS)
        pair = (book_id, reader_id)
        if pair not in book_reader_pairs:
            book_reader_pairs.add(pair)
            book_readers.append({"book_id": book_id, "reader_id": reader_id})
            break


# Запись данных в CSV-файлы
def write_csv(filename, data, headers):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)


# Запись authors.csv
write_csv(
    "authors.csv", authors, ["author_id", "first_name", "last_name", "nationality"]
)

# Запись books.csv
write_csv(
    "books.csv",
    books,
    ["book_id", "title", "publication_year", "category", "author_id"],
)

# Запись readers.csv
write_csv("readers.csv", readers, ["reader_id", "first_name", "last_name", "email"])

# Запись book_readers.csv
write_csv("book_readers.csv", book_readers, ["book_id", "reader_id"])

print(
    "CSV-файлы успешно сгенерированы: authors.csv, books.csv, readers.csv, book_readers.csv"
)
