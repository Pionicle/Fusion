import psycopg2
from psycopg2 import Error
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Параметры подключения к базе данных
db_params = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5434",
}

# Список таблиц и соответствующих CSV-файлов с колонками
tables = [
    {
        "table_name": "authors",
        "csv_file": "authors.csv",
        "columns": ("author_id", "first_name", "last_name", "nationality"),
    },
    {
        "table_name": "books",
        "csv_file": "books.csv",
        "columns": ("book_id", "title", "publication_year", "category", "author_id"),
    },
    {
        "table_name": "readers",
        "csv_file": "readers.csv",
        "columns": ("reader_id", "first_name", "last_name", "email"),
    },
    {
        "table_name": "book_readers",
        "csv_file": "book_readers.csv",
        "columns": ("book_id", "reader_id"),
    },
]

create_script = """
CREATE TYPE NATIONALITY AS ENUM ('Russian', 'American', 'British', 'French', 'German');

CREATE TABLE authors (
    author_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    nationality NATIONALITY NOT NULL
);

CREATE TYPE BOOK_CATEGORY AS ENUM ('Fiction', 'Non-fiction', 'Science', 'History', 'Fantasy');

CREATE TABLE books (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(50) UNIQUE NOT NULL,
    publication_year DATE NOT NULL,
    category BOOK_CATEGORY NOT NULL,
    author_id INT,
    CONSTRAINT fk_author FOREIGN KEY (author_id) REFERENCES authors (author_id) ON DELETE SET NULL
);

CREATE TABLE readers (
    reader_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    CONSTRAINT valid_email CHECK (
        email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    )
);

CREATE TABLE book_readers (
    book_id INT,
    reader_id INT,
    CONSTRAINT fk_book FOREIGN KEY (book_id) REFERENCES books (book_id) ON DELETE CASCADE,
    CONSTRAINT fk_reader FOREIGN KEY (reader_id) REFERENCES readers (reader_id) ON DELETE CASCADE,
    PRIMARY KEY (book_id, reader_id)
);
"""

synchronize_script = """
SELECT setval(
        'authors_author_id_seq', (
            SELECT COALESCE(MAX(author_id), 0)
            FROM authors
        )
    );

SELECT setval(
        'books_book_id_seq', (
            SELECT COALESCE(MAX(book_id), 0)
            FROM books
        )
    );

SELECT setval('readers_reader_id_seq', (
            SELECT COALESCE(MAX(reader_id), 0)
            FROM readers
        )
    );
"""


def check_table_exists(cursor, table_name):
    """Проверка существования таблицы в базе данных."""
    cursor.execute(
        """
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = %s
        );
    """,
        (table_name,),
    )
    return cursor.fetchone()[0]


def import_csv_to_table(cursor, table_name, csv_file, columns):
    """Импорт данных из CSV в указанную таблицу, пустые строки интерпретируются как NULL."""
    try:
        with open(csv_file, "r", encoding="utf-8") as f:
            next(f)  # Пропускаем заголовок
            cursor.copy_from(f, table_name, sep=",", columns=columns, null="")
        logger.info(f"Successfully imported data from {csv_file} into {table_name}")
    except FileNotFoundError:
        logger.error(f"File {csv_file} not found")
        raise
    except Exception as e:
        logger.error(f"Error importing {csv_file} into {table_name}: {str(e)}")
        raise


def main():
    # Подключение к базе данных
    conn = None
    cur = None
    try:
        logger.info("Connecting to the database...")
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Импорт данных для каждой таблицы
        for table in tables:
            table_name = table["table_name"]
            csv_file = table["csv_file"]
            columns = table["columns"]

            # Проверка существования таблицы
            if not check_table_exists(cur, table_name):
                cur.execute(create_script)

            logger.info(f"Importing data into {table_name} from {csv_file}...")
            import_csv_to_table(cur, table_name, csv_file, columns)

        # Подтверждение транзакции
        conn.commit()
        # Синхронизация последовательности для таблиц
        cur.execute(synchronize_script)
        logger.info("All data imported successfully")

    except (Exception, Error) as error:
        logger.error(f"Database error: {str(error)}")
        if conn:
            conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
            logger.info("Database connection closed")


if __name__ == "__main__":
    main()
