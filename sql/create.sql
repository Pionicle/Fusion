CREATE TYPE NATIONALITY AS ENUM ('Russian', 'American', 'British', 'French', 'German');

CREATE TABLE authors (
    author_id SERIAL PRIMARY KEY,
    first_name VARCHAR (50) NOT NULL,
    last_name VARCHAR (50) NOT NULL,
    nationality NATIONALITY NOT NULL
);

CREATE TYPE BOOK_CATEGORY AS ENUM ('Fiction', 'Non-fiction', 'Science', 'History', 'Fantasy');

CREATE TABLE books (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR (50) UNIQUE NOT NULL,
    publication_year DATE NOT NULL,
    category BOOK_CATEGORY NOT NULL,
    author_id INT, 
    CONSTRAINT fk_author
        FOREIGN KEY(author_id)
        REFERENCES authors(author_id)
        ON DELETE SET NULL
);


CREATE TABLE readers (
    reader_id SERIAL PRIMARY KEY,
    first_name VARCHAR (50) NOT NULL,
    last_name VARCHAR (50) NOT NULL,
    email VARCHAR (255) UNIQUE NOT NULL,
    CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

CREATE TABLE book_readers (
    book_id INT,
    reader_id INT,
    CONSTRAINT fk_book
        FOREIGN KEY(book_id)
        REFERENCES books(book_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_reader
        FOREIGN KEY(reader_id)
        REFERENCES readers(reader_id)
        ON DELETE CASCADE,
    PRIMARY KEY (book_id, reader_id)
);