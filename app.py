import os
from database import (
    is_database_empty,
    table_exists,
    create_table,
    load_data_from_csv,
)
from flask import Flask

app = Flask(__name__)


def init_db():
    table_name = "contacts"
    path2csv = "Nimble Contacts - Sheet1.csv"

    if not os.path.exists(path2csv):
        raise FileNotFoundError(f"File {path2csv} not found.")

    if table_exists(table_name) and not is_database_empty(table_name):
        print("Database already contains data. Initialization skipped.")
        return

    create_table(table_name)
    load_data_from_csv(table_name, path2csv)
    print("Database initialized and data loaded successfully.")


@app.route("/")
def view():
    return "Hello, Flask is up and running!"


if __name__ == "__main__":
    try:
        init_db()
        app.run(host="0.0.0.0", port=5000)
    except Exception as e:
        print(f"Error during initialization: {e}")
