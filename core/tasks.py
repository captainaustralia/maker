from maker.celery import app
from .services import delete_inactive_user


@app.task
def delete_inactive_beat():
    delete_inactive_user()

