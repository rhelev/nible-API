from config import TABLE_NAME
from database import (
    get_db_connection,
    is_database_empty,
    table_exists,
    create_table,
    load_data_from_csv,
)
from flask import Flask, request, jsonify
import os

app = Flask(__name__)


def init_db():
    """
    Create contacts db from csv file, if not exists
    """
    path2csv = "Nimble Contacts - Sheet1.csv"

    if not os.path.exists(path2csv):
        raise FileNotFoundError(f"File {path2csv} not found.")

    if table_exists(TABLE_NAME) and not is_database_empty(TABLE_NAME):
        print("Database already contains data. Initialization skipped.")
        return

    create_table(TABLE_NAME)
    load_data_from_csv(TABLE_NAME, path2csv)
    print("Database initialized and data loaded successfully.")


@app.route("/search", methods=["GET"])
def search_contacts():
    # Get the search query from the request parameters
    query = request.args.get("q", "")
    # Perform the full-text search
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            sql = f"""
                SELECT first_name, last_name, email
                FROM {TABLE_NAME}
                WHERE to_tsvector('english', first_name || ' ' || last_name || ' ' || email) @@ to_tsquery('english', %s)
            """
            cursor.execute(sql, (query,))
            results = cursor.fetchall()

    # Serialize the results into a list of dictionaries
    contacts = [
        {
            "first_name": contact[0],
            "last_name": contact[1],
            "email": contact[2],
        }
        for contact in results
    ]

    return jsonify(contacts)


@app.route("/")
def view():
    return "Hello, Flask is up and running!"


if __name__ == "__main__":
    try:
        init_db()
        app.run(host="0.0.0.0", port=5000)
    except Exception as e:
        print(f"Error during initialization: {e}")
