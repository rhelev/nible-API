from celery import Celery
import scheduler.celeryconfig as celeryconfig
from scheduler.update_contacts_task import (
    update_contacts,
    get_contacts_for_update,
)
from flask import Flask

app = Flask(__name__)
app.config.from_object("config")


celery = Celery(app.import_name, broker=app.config["BROKER_URL"])
celery.config_from_object(celeryconfig)


@celery.task(name="update_contacts")
def update_db():
    contacts_data = get_contacts_for_update(
        app.config["API_URL"], app.config["API_HEADERS"]
    )
    if contacts_data:
        update_contacts(contacts_data)
