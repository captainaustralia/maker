from maker.celery import app
from .services import delete_inactive_user


@app.task
def delete_inactive_beat():
    """
    Beat(every day) task , for delete all user ,
    if field -> is_active = False
    """
    delete_inactive_user()
