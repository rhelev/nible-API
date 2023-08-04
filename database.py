import csv
import psycopg2


def get_db_connection():
    # Establishes a connection to the PostgreSQL database.
    connection = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="mysecretpassword",
        host="localhost",
        port="5432",
    )
    return connection


def is_database_empty(table_name):
    # Checks if the specified table in the database is empty.
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM {table_name};")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count == 0


def table_exists(table_name):
    # Checks if the specified table exists in the database.
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        f"SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}')"
    )
    exists = cur.fetchone()[0]
    cur.close()
    conn.close()
    return exists


def create_table(table_name):
    # Creates the table with first_name, last_name, and email columns if it does not exist.
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        );
    """
    )
    conn.commit()
    cur.close()
    conn.close()


def load_data_from_csv(table_name, path2csv):
    # Loads data from CSV file into the specified table in the database.
    with open(path2csv, "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        conn = get_db_connection()
        cur = conn.cursor()
        for row in reader:
            cur.execute(
                f"INSERT INTO {table_name} (first_name, last_name, email) VALUES (%s, %s, %s)",
                row,
            )
        conn.commit()
        cur.close()
        conn.close()
