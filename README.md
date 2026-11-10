# COMP 3005 - Assignment 3, Question 1

I wrote a small Python application that connects to a PostgreSQL database and performs the four required CRUD operations on the `students` table.

Demonstration video: TODO add link

## Repository layout

```
db/schema.sql   creates the students table and loads the initial data
main.py         the application: connection, the four functions, and a menu to call them
requirements.txt
```

## Requirements

- PostgreSQL (I used 16)
- Python 3.10 or newer
- The `psycopg` 3 driver, which `requirements.txt` installs

## Setup

1. Create the database.

   ```sh
   createdb comp3005_a3
   ```

2. Create the table and load the initial data.

   ```sh
   psql -d comp3005_a3 -f db/schema.sql
   ```

## Compile and run

Python is interpreted, so there is nothing to compile. Set up the dependencies and run the program:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

The program connects to the database, then shows a menu that calls each function:

```
  1. List all students        (getAllStudents)
  2. Add a student            (addStudent)
  3. Update a student's email (updateStudentEmail)
  4. Delete a student         (deleteStudent)
  5. Quit
```

The connection settings are read from environment variables, so no credentials are stored in the code:

| Variable | Default |
| --- | --- |
| `PGHOST` | `localhost` |
| `PGPORT` | `5432` |
| `PGDATABASE` | `comp3005_a3` |
| `PGUSER` | your system user name |
| `PGPASSWORD` | empty |

On a machine where PostgreSQL runs on another port, for example, run the program with `PGPORT=5416 python main.py`.

## Functions

Each function takes the open database connection as its first argument.

- `getAllStudents()` retrieves every row of the `students` table and prints it as a table ordered by `student_id`.
- `addStudent(first_name, last_name, email, enrollment_date)` inserts a new student. `student_id` is assigned by the database, and `enrollment_date` is a `YYYY-MM-DD` string or nothing if the date is unknown.
- `updateStudentEmail(student_id, new_email)` changes the email of one student and reports the new value.
- `deleteStudent(student_id)` removes one student and reports which record was deleted.

Each function reports a clear message when no student matches the given id, and the program keeps running after a rejected input such as a duplicate email or a blank name.
