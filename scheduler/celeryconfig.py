from datetime import timedelta

beat_schedule = {
    "update_contacts": {
        "task": "update_contacts",
        "schedule": timedelta(seconds=5),
    }
}
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "UTC"
enable_utc = True
broker_connection_retry_on_startup = True
