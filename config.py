"""Broker config"""
REDIS_HOST = "broker"
REDIS_PORT = 6379
BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
CELERY_RESULT_BACKEND = BROKER_URL

"""API config"""
API_URL = "https://api.nimble.com/api/v1/contacts/"
API_KEY = "NxkA2RlXS3NiR8SKwRdDmroA992jgu"
API_HEADERS = {"Authorization": f"Bearer {API_KEY}"}

"""DB config"""
TABLE_NAME = "contacts"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "mysecretpassword"
DB_HOST = "localhost"
DB_PORT = "5432"
