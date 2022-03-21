from maker.celery import app
from .services import delete_inactive_user


@app.task
def delete_inactive():
    delete_inactive_user()
