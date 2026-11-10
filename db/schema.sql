-- COMP 3005 - Assignment 3, Question 1
--
-- Creates the students table exactly as specified in the assignment and loads
-- the initial data. Run it with:
--
--     psql -d comp3005_a3 -f db/schema.sql
--
-- The DROP lets me run the script again from a clean state.

DROP TABLE IF EXISTS students;

CREATE TABLE students (
    student_id      SERIAL PRIMARY KEY,   -- integer primary key, auto-increment
    first_name      TEXT NOT NULL,
    last_name       TEXT NOT NULL,
    email           TEXT NOT NULL UNIQUE,
    enrollment_date DATE
);

-- Initial data provided in the assignment. student_id is left out because
-- SERIAL assigns it (1, 2, 3 in the order inserted).
INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
    ('John', 'Doe',   'john.doe@example.com',   '2023-09-01'),
    ('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
    ('Jim',  'Beam',  'jim.beam@example.com',   '2023-09-02');
