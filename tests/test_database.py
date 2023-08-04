import unittest
import database


class TestDatabaseFunctions(unittest.TestCase):
    def setUp(self):
        # Set up the database connection before each test
        self.conn = database.get_db_connection()
        self.cur = self.conn.cursor()

    def tearDown(self):
        # Close the database connection after each test
        self.cur.close()
        self.conn.close()

    def test_create_table(self):
        # Test if the table is created successfully
        table_name = "test_table"
        database.create_table(table_name)

        # Check if the table exists in the database
        self.assertTrue(database.table_exists(table_name))

    def test_table_exists(self):
        # Test if the table exists in the database
        table_name = "test_table"
        self.assertTrue(database.table_exists(table_name))

    def test_is_database_empty(self):
        # Test if the database is empty
        table_name = "test_table"
        self.assertTrue(database.is_database_empty(table_name))

    def test_load_data_from_csv(self):
        # Test if data is loaded successfully from the CSV file
        table_name = "test_table"
        csv_file = "Nimble Contacts - Sheet1.csv"
        database.create_table(table_name)
        database.load_data_from_csv(table_name, csv_file)

        # Check if the table is not empty after data loading
        self.assertFalse(database.is_database_empty(table_name))


if __name__ == "__main__":
    unittest.main()
