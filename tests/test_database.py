import unittest
import database


class TestDatabaseFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the database connection once for the entire test class
        cls.conn = database.get_db_connection()
        cls.cur = cls.conn.cursor()

    @classmethod
    def tearDownClass(cls):
        # Close the database connection once after all tests in the class are done
        cls.cur.close()
        cls.conn.close()

    def setUp(self):
        # Create a new table before each test
        self.table_name = "test_table"
        database.create_table(self.table_name)

    def tearDown(self):
        # Drop the table after each test
        with self.conn:
            self.cur.execute(f"DROP TABLE IF EXISTS {self.table_name}")

    def test_create_table(self):
        # Test if the table is created successfully
        self.assertTrue(database.table_exists(self.table_name))

    def test_table_exists(self):
        # Test if the table exists in the database
        self.assertTrue(database.table_exists(self.table_name))

    def test_is_database_empty(self):
        # Test if the database is empty
        self.assertTrue(database.is_database_empty(self.table_name))

    def test_load_data_from_csv(self):
        # Test if data is loaded successfully from the CSV file
        csv_file = "Nimble Contacts - Sheet1.csv"
        database.load_data_from_csv(self.table_name, csv_file)

        # Check if the table is not empty after data loading
        self.assertFalse(database.is_database_empty(self.table_name))


if __name__ == "__main__":
    unittest.main()
