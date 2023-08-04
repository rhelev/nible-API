import requests
from database import get_db_connection
import psycopg2


def get_resource_field_value(resource, field_name, default_value=None):
    fields_dict = resource.get("fields", {})
    field_list = fields_dict.get(field_name, [])
    return field_list[0].get("value") if field_list else default_value


def get_contacts_for_update(api_url, headers):
    # Make the request to the API
    contacts = []
    try:
        response = requests.get(api_url, headers=headers)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Process the API response data here
            data = response.json()
            resources = data.get("resources")
            for resource in resources:
                email = get_resource_field_value(resource, "email")
                # skip contacts without email
                if not email:
                    continue
                first_name = get_resource_field_value(resource, "first name")
                last_name = get_resource_field_value(resource, "last name")
                contacts.append(
                    {
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                    }
                )
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
    return contacts


def update_contacts(contacts_data):
    try:
        connection = get_db_connection()

        cursor = connection.cursor()

        sql = """
            INSERT INTO contacts (first_name, last_name, email)
            VALUES (%s, %s, %s)
            ON CONFLICT (email) DO UPDATE
            SET first_name = EXCLUDED.first_name,
                last_name = EXCLUDED.last_name
        """

        # Convert contacts_data into a list of tuples (first_name, last_name, email)
        data = [
            (contact["first_name"], contact["last_name"], contact["email"])
            for contact in contacts_data
        ]
        cursor.executemany(sql, data)
        connection.commit()

        print("Bulk contacts update successfully!")

    except (Exception, psycopg2.Error) as error:
        print(f"Error updating contacts: {error}")

    finally:
        if connection:
            cursor.close()
            connection.close()


if __name__ == "__main__":
    api_url = "https://api.nimble.com/api/v1/contacts/"
    api_key = "NxkA2RlXS3NiR8SKwRdDmroA992jgu"
    headers = {"Authorization": f"Bearer {api_key}"}
    contacts_data = get_contacts_for_update(api_url, headers)
    if contacts_data:
        update_contacts(contacts_data)
