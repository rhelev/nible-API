# nimble-task
Contact service for Nimble

# Commands
Start app
> python app.py
Start celery worker
> celery -A scheduler.celery worker -B
Run tests
> python -m unittest discover tests

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