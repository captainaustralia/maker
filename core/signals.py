from django.db.models.signals import post_save
from django.dispatch import receiver
from djoser.signals import user_activated, user_registered

from core.models import Company, User
from maker import settings


@receiver(user_activated)
def create_profile(sender, user, request, **kwargs):
    pass

