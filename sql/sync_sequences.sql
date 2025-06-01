-- Синхронизация последовательности для таблицы authors
SELECT setval(
        'authors_author_id_seq', (
            SELECT COALESCE(MAX(author_id), 0)
            FROM authors
        )
    );

-- Синхронизация последовательности для таблицы books
SELECT setval(
        'books_book_id_seq', (
            SELECT COALESCE(MAX(book_id), 0)
            FROM books
        )
    );

-- Синхронизация последовательности для таблицы readers
SELECT setval(
        'readers_reader_id_seq', (
            SELECT COALESCE(MAX(reader_id), 0)
            FROM readers
        )
    );