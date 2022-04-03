import datetime
import os

from .models import User


def delete_inactive_user():
    """
    Functions for delete all users,
    if they have flag is_active = False
    """
    inactive_user = User.objects.filter(last_login__isnull=True, is_superuser=False, is_active=False,
                                        date_register__day__lt=datetime.date.day)

    #  additional verification
    for i in inactive_user:
        if i.date_register > datetime.date.today():
            return 0
        else:
            inactive_user.delete()


