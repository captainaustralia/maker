import django.db.models.base
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_staff=False, is_admin=False, active=True):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(
            email=self.normalize_email(email)
        )
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = active
        user_obj.set_password(password)
        user_obj.save()
        return user_obj

    def create_staffuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,

            password=password,
            is_staff=True,
            is_admin=True
        )
        return user


class User(AbstractBaseUser):
    """Base User model """
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False
    )
    """E-mail + pass -> auth fields"""

    phone = PhoneNumberField(
        blank=False
    )

    first_name = models.CharField(
        max_length=30,
        blank=False
    )

    last_name = models.CharField(
        max_length=30,
        blank=False
    )

    country = models.CharField(
        max_length=30,
        blank=False
    )

    city = models.CharField(
        max_length=30,
        blank=False
    )
    """Maybe worth create table 'Location' idk, but now we can send ajax to API postman or other"""
    """???"""
    """Also maybe need postpone about/first_name/last_name in profile"""
    """2 step register, 1 - email/pass/phone/city , 2 - profile info: firstname/lastname/about/avatar"""
    about = models.TextField(
        max_length=200,
        blank=True
    )
    """Field for write about info"""
    user_confirm = models.BooleanField(
        default=False
    )
    """After registration, we will send a confirmation link to mail, after confirmation, the flag will be changed"""

    active = models.BooleanField(default=True)
    """Flag that change when user want delete his account """

    admin = models.BooleanField(default=False)
    """Admin flag"""

    staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    """A setting that says what will be the name identifier during authorization"""

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
