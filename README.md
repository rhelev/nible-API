# nimble-task
Contact service for Nimble

# Commands
Run app
```
python app.py
```
Run celery worker
```
celery -A scheduler.celery worker -B
```
Run tests
```
python -m unittest discover tests
```

# API Documentation: Search Contacts
#### Endpoint
> GET /search

#### Description
> Searches for contacts in the database based on the provided query.

#### Parameters
```
+----------------------------------------------------------------+
|   Parameter |  Type     | Description                          |
+----------------------------------------------------------------+
|   q         |  string   | The search query to filter contacts. |
+----------------------------------------------------------------+
```

#### Usage
> You can use the search_contacts endpoint to search for contacts by their first name, last name, or email. Simply provide the q parameter with your search query, and the API will return a list of contacts that match the query.

#### Example Request
```
GET /search?q=john
```

#### Example Response
```
[
    {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    }
]
```