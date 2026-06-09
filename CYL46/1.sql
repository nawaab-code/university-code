-- ================================================================
-- Library Database  |  Question 1
-- Run: mysql -u root -p < library.sql
-- Explore: mysql -u root -p library_db
-- ================================================================

DROP DATABASE IF EXISTS library_db;
CREATE DATABASE library_db;
USE library_db;

-- ────────────────────────────────────────────────
-- TABLES  (parent tables first, then child tables)
-- ────────────────────────────────────────────────

CREATE TABLE PUBLISHER (
    Name            VARCHAR(100) PRIMARY KEY,
    Address         VARCHAR(200),
    Phone           VARCHAR(15)
);

CREATE TABLE BOOK (
    Book_id         INT PRIMARY KEY,
    Title           VARCHAR(200),
    Publisher_Name  VARCHAR(100),
    Pub_Year        YEAR,
    FOREIGN KEY (Publisher_Name) REFERENCES PUBLISHER(Name)
);

CREATE TABLE BOOK_AUTHORS (
    Book_id         INT,
    Author_Name     VARCHAR(100),
    PRIMARY KEY (Book_id, Author_Name),
    FOREIGN KEY (Book_id) REFERENCES BOOK(Book_id)
);

CREATE TABLE LIBRARY_BRANCH (
    Branch_id       INT PRIMARY KEY,
    Branch_Name     VARCHAR(100),
    Address         VARCHAR(200)
);

CREATE TABLE BOOK_COPIES (
    Book_id         INT,
    Branch_id       INT,
    No_of_Copies    INT,
    PRIMARY KEY (Book_id, Branch_id),
    FOREIGN KEY (Book_id)   REFERENCES BOOK(Book_id),
    FOREIGN KEY (Branch_id) REFERENCES LIBRARY_BRANCH(Branch_id)
);

CREATE TABLE BOOK_LENDING (
    Book_id         INT,
    Branch_id       INT,
    Card_No         INT,
    Date_Out        DATE,
    Due_Date        DATE,
    PRIMARY KEY (Book_id, Branch_id, Card_No),
    FOREIGN KEY (Book_id)   REFERENCES BOOK(Book_id),
    FOREIGN KEY (Branch_id) REFERENCES LIBRARY_BRANCH(Branch_id)
);

-- ────────────────────────────────────────────────
-- DATA
-- ────────────────────────────────────────────────

INSERT INTO PUBLISHER VALUES
('McGraw Hill', 'New York',      '1111111111'),
('Pearson',     'London',        '2222222222'),
('Wiley',       'Chicago',       '3333333333'),
('OReilly',     'San Francisco', '4444444444'),
('Springer',    'Berlin',        '5555555555');

INSERT INTO BOOK VALUES
(1, 'DBMS Concepts',     'McGraw Hill', 2015),
(2, 'Operating Systems', 'Pearson',     2018),
(3, 'Data Structures',   'Wiley',       2012),
(4, 'Computer Networks', 'OReilly',     2020),
(5, 'Algorithm Design',  'Springer',    2017),
(6, 'Database Design',   'Pearson',     2019);

INSERT INTO BOOK_AUTHORS VALUES
(1, 'Elmasri Navathe'),
(2, 'Silberschatz'),
(3, 'Mark Allen Weiss'),
(4, 'Andrew Tanenbaum'),
(5, 'Cormen'),
(6, 'Ramez Elmasri');

INSERT INTO LIBRARY_BRANCH VALUES
(1, 'Central Branch', 'MG Road'),
(2, 'North Branch',   'JP Nagar'),
(3, 'South Branch',   'Koramangala'),
(4, 'East Branch',    'Whitefield'),
(5, 'West Branch',    'Rajajinagar');

-- Branch 1 has all 6 books; other branches have subsets
INSERT INTO BOOK_COPIES VALUES
(1, 1, 5), (2, 1, 3), (3, 1, 4), (4, 1, 3), (5, 1, 5), (6, 1, 8),
(1, 2, 3), (2, 2, 2), (3, 2, 7),
(4, 3, 4), (5, 3, 3),
(5, 4, 6);

-- NOTE: Card 101 borrows 5 books from Branch 1 between Jan-Jun 2026
--       → triggers query ii  (borrowed > 3 books in that date range)
--       Branch 1 accumulates 9 total lendings in 2026
--       → triggers query iv  (branch lent > 6 books in a year)
INSERT INTO BOOK_LENDING VALUES
(1, 1, 101, '2026-01-10', '2026-02-10'),
(2, 1, 101, '2026-02-05', '2026-03-05'),
(3, 1, 101, '2026-03-15', '2026-04-15'),
(4, 1, 101, '2026-04-01', '2026-05-01'),
(5, 1, 101, '2026-05-10', '2026-06-10'),
(6, 1, 102, '2026-01-20', '2026-02-20'),
(3, 1, 103, '2026-03-01', '2026-04-01'),
(5, 1, 104, '2026-05-20', '2026-06-20'),
(6, 1, 105, '2026-06-01', '2026-07-01'),
(1, 2, 102, '2026-02-15', '2026-03-15'),
(2, 2, 103, '2026-04-10', '2026-05-10'),
(4, 3, 104, '2025-11-01', '2025-12-01');  -- older record, different year

-- ────────────────────────────────────────────────
-- VERIFY  (run these manually inside mysql shell)
-- ────────────────────────────────────────────────
-- SHOW TABLES;
-- SELECT * FROM PUBLISHER;
-- SELECT * FROM BOOK;
-- SELECT * FROM BOOK_AUTHORS;
-- SELECT * FROM LIBRARY_BRANCH;
-- SELECT * FROM BOOK_COPIES;
-- SELECT * FROM BOOK_LENDING;
-- DESCRIBE BOOK_LENDING;   -- shows column types and keys