# nimble-task
Contact service for Nimble
# Commands
Start app
> python app.py
Start celery worker
> celery -A scheduler.celery worker -B
Run tests
> python -m unittest discover tests