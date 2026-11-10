"""COMP 3005 - Assignment 3, Question 1

A command-line application that connects to a PostgreSQL database and performs
the four required operations on the students table.

Run it with:  python main.py
"""

import os
import sys

import psycopg


def connect():
    """Open a connection to the database.

    I read the settings from environment variables so the database password
    never has to be written in the source code. The defaults are for a local
    PostgreSQL install; see README.md for the variables.
    """
    return psycopg.connect(
        host=os.environ.get("PGHOST", "localhost"),
        port=os.environ.get("PGPORT", "5432"),
        dbname=os.environ.get("PGDATABASE", "comp3005_a3"),
        user=os.environ.get("PGUSER", os.environ.get("USER", "postgres")),
        password=os.environ.get("PGPASSWORD") or None,
        # I commit every statement as it runs, so each change is already saved
        # and visible in pgAdmin when the menu prints the result.
        autocommit=True,
    )


# ---------------------------------------------------------------------------
# The four required functions
# ---------------------------------------------------------------------------


def getAllStudents(conn):
    """Retrieve and display all records in the students table."""
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT student_id, first_name, last_name, email, enrollment_date
            FROM students
            ORDER BY student_id
            """
        )
        rows = cur.fetchall()

    if not rows:
        print("The students table is empty.")
        return

    # Print the rows in a table so the output is easy to read in the terminal.
    print(
        f"{'student_id':<12}{'first_name':<14}{'last_name':<14}"
        f"{'email':<30}{'enrollment_date'}"
    )
    print("-" * 80)
    for student_id, first_name, last_name, email, enrollment_date in rows:
        print(
            f"{student_id:<12}{first_name:<14}{last_name:<14}"
            f"{email:<30}{enrollment_date or ''}"
        )
    print(f"\n{len(rows)} student(s).")


def addStudent(conn, first_name, last_name, email, enrollment_date):
    """Insert a new student record into the students table.

    enrollment_date is a 'YYYY-MM-DD' string, or None if the date is unknown.
    """
    # NOT NULL in the table stops NULL values, but not empty strings, so I
    # reject blank input here instead of storing a nameless student.
    if not first_name.strip() or not last_name.strip() or not email.strip():
        print("First name, last name and email cannot be empty.")
        return

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO students (first_name, last_name, email, enrollment_date)
            VALUES (%s, %s, %s, %s)
            RETURNING student_id
            """,
            (first_name, last_name, email, enrollment_date or None),
        )
        student_id = cur.fetchone()[0]

    print(f"Added student {student_id}.")


def updateStudentEmail(conn, student_id, new_email):
    """Update the email address of the student with the given student_id."""
    if not new_email.strip():
        print("The new email cannot be empty.")
        return

    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE students
            SET email = %s
            WHERE student_id = %s
            RETURNING first_name, last_name
            """,
            (new_email, student_id),
        )
        row = cur.fetchone()

    # An UPDATE that matches no row is not a success, so I say so instead of
    # showing a confirmation for a student that does not exist.
    if row is None:
        print(f"No student with id {student_id}.")
    else:
        print(f"Student {student_id} ({row[0]} {row[1]}) now has email {new_email}.")


def deleteStudent(conn, student_id):
    """Delete the record of the student with the given student_id."""
    with conn.cursor() as cur:
        cur.execute(
            """
            DELETE FROM students
            WHERE student_id = %s
            RETURNING first_name, last_name
            """,
            (student_id,),
        )
        row = cur.fetchone()

    if row is None:
        print(f"No student with id {student_id}.")
    else:
        print(f"Deleted student {student_id} ({row[0]} {row[1]}).")


# ---------------------------------------------------------------------------
# Menu
# ---------------------------------------------------------------------------


def read_student(conn):
    """Ask for the fields of a new student and add it to the table."""
    first_name = input("First name: ").strip()
    last_name = input("Last name: ").strip()
    email = input("Email: ").strip()
    enrollment_date = input("Enrollment date (YYYY-MM-DD, blank for none): ").strip()
    addStudent(conn, first_name, last_name, email, enrollment_date)


def read_student_email(conn):
    """Ask for a student id and a new email address, then update it."""
    student_id = read_id()
    new_email = input("New email: ").strip()
    updateStudentEmail(conn, student_id, new_email)


def read_student_to_delete(conn):
    """Ask for a student id and delete that student."""
    student_id = read_id()
    deleteStudent(conn, student_id)


def read_id():
    """Read a student id from the keyboard, reprompting until it is a number."""
    while True:
        value = input("Student id: ").strip()
        try:
            return int(value)
        except ValueError:
            print("Please type a number.")


def main():
    """Connect to the database and show the menu until the user quits."""
    try:
        conn = connect()
    except psycopg.Error as exc:
        # The most common cause is a wrong database name or server not running.
        print(f"Could not connect to the database: {str(exc).splitlines()[0]}")
        print("Check your PG* environment variables and that db/schema.sql has run.")
        return 1

    actions = {
        "1": getAllStudents,
        "2": read_student,
        "3": read_student_email,
        "4": read_student_to_delete,
    }

    try:
        while True:
            print(
                "\nCOMP 3005 - Assignment 3, Question 1\n"
                "  1. List all students        (getAllStudents)\n"
                "  2. Add a student            (addStudent)\n"
                "  3. Update a student's email (updateStudentEmail)\n"
                "  4. Delete a student         (deleteStudent)\n"
                "  5. Quit"
            )
            choice = input("Choose an option: ").strip()

            if choice in ("5", "q"):
                return 0

            action = actions.get(choice)
            if action is None:
                print("Please choose 1-5.")
                continue

            # One try block around each action keeps a bad value, a duplicate
            # email or a lost connection from ending the whole program.
            try:
                action(conn)
            except psycopg.errors.UniqueViolation:
                print("That email already belongs to another student.")
            except psycopg.Error as exc:
                print(f"Database error: {str(exc).splitlines()[0]}")
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
