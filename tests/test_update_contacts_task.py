import unittest
from unittest.mock import patch, MagicMock
from scheduler.update_contacts_task import (
    get_contacts_for_update,
    update_contacts,
    get_resource_field_value,
)


class TestContactsFunctions(unittest.TestCase):
    @patch("scheduler.update_contacts_task.requests.get")
    def test_get_contacts_for_update(self, mock_get):
        # Set up the mock response for requests.get
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "resources": [
                {
                    "fields": {
                        "email": [{"value": "john@example.com"}],
                        "first name": [{"value": "John"}],
                        "last name": [{"value": "Doe"}],
                    }
                },
                {
                    "fields": {
                        "email": [{"value": "jane@example.com"}],
                        "first name": [{"value": "Jane"}],
                        "last name": [{"value": "Smith"}],
                    }
                },
            ]
        }
        mock_get.return_value = mock_response

        # Call the function to get contacts for update
        api_url = "https://mockapi.com/api/v1/contacts/"
        headers = {"Authorization": "Bearer mock_token"}
        contacts_data = get_contacts_for_update(api_url, headers)

        # Assert that the mock get request was called with the correct arguments
        mock_get.assert_called_once_with(api_url, headers=headers)

        # Assert that the returned contacts_data contains the expected data
        expected_contacts_data = [
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@example.com",
            },
            {
                "first_name": "Jane",
                "last_name": "Smith",
                "email": "jane@example.com",
            },
        ]
        self.assertEqual(contacts_data, expected_contacts_data)

    @patch("scheduler.update_contacts_task.get_db_connection")
    def test_update_contacts(self, mock_get_db_connection):
        # Set up the mock database connection and cursor
        mock_connection = MagicMock()
        mock_cursor = mock_connection.cursor.return_value
        mock_get_db_connection.return_value = mock_connection

        # Call the function to update contacts
        contacts_data = [
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@example.com",
            },
            {
                "first_name": "Jane",
                "last_name": "Smith",
                "email": "jane@example.com",
            },
        ]
        update_contacts(contacts_data)

        # Assert that the database connection and cursor were used correctly
        mock_get_db_connection.assert_called_once()
        mock_connection.cursor.assert_called_once()
        mock_cursor.executemany.assert_called_once()
        mock_connection.commit.assert_called_once()


class TestGetResourceFieldValue(unittest.TestCase):
    def test_get_existing_field(self):
        # Test when the field exists in the resource dictionary
        resource = {
            "fields": {
                "email": [{"value": "john@example.com"}],
                "first name": [{"value": "John"}],
                "last name": [{"value": "Doe"}],
            }
        }
        field_name = "email"
        expected_value = "john@example.com"

        result = get_resource_field_value(resource, field_name)

        self.assertEqual(result, expected_value)

    def test_get_non_existing_field_with_default_value(self):
        # Test when the field does not exist in the resource dictionary,
        # but a default value is provided
        resource = {
            "fields": {
                "first name": [{"value": "John"}],
                "last name": [{"value": "Doe"}],
            }
        }
        field_name = "email"
        default_value = "default@example.com"

        result = get_resource_field_value(resource, field_name, default_value)

        self.assertEqual(result, default_value)

    def test_get_non_existing_field_without_default_value(self):
        # Test when the field does not exist in the resource dictionary,
        # and no default value is provided
        resource = {
            "fields": {
                "first name": [{"value": "John"}],
                "last name": [{"value": "Doe"}],
            }
        }
        field_name = "email"

        result = get_resource_field_value(resource, field_name)

        self.assertIsNone(result)

    def test_empty_field_list_with_default_value(self):
        # Test when the field list is empty, but a default value is provided
        resource = {
            "fields": {
                "email": [],
                "first name": [{"value": "John"}],
                "last name": [{"value": "Doe"}],
            }
        }
        field_name = "email"
        default_value = "default@example.com"

        result = get_resource_field_value(resource, field_name, default_value)

        self.assertEqual(result, default_value)

    def test_empty_field_list_without_default_value(self):
        # Test when the field list is empty, and no default value is provided
        resource = {
            "fields": {
                "email": [],
                "first name": [{"value": "John"}],
                "last name": [{"value": "Doe"}],
            }
        }
        field_name = "email"

        result = get_resource_field_value(resource, field_name)

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
