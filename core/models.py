import datetime
import django.db.models.base
import pycountry
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from multiselectfield import MultiSelectField
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.timezone import now


class UserManager(BaseUserManager):
    def create_user(self, email, password, is_staff=False, is_admin=False, is_active=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(
            email=self.normalize_email(email)
        )
        user_obj.is_staff = is_staff
        user_obj.is_admin = is_admin
        user_obj.is_active = is_active
        user_obj.set_password(password)
        user_obj.save()
        return user_obj

    def create_staffuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
            is_staff=True,
            is_admin=True,
            is_active=True
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

    is_active = models.BooleanField(default=True)
    """Flag that change when user want delete his account """

    is_admin = models.BooleanField(default=False)
    """Admin flag"""

    is_staff = models.BooleanField(default=False)

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

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Company(models.Model):
    name = models.CharField(
        max_length=255
    )
    phone = PhoneNumberField(
        unique=True,
        blank=False
    )
    description = models.CharField(
        max_length=1155,
        blank=False
    )
    email = models.EmailField(
        max_length=255,
        blank=False
    )

    start_date = models.DateTimeField(default=now())
    end_date = models.DateTimeField()  # not sure about format
    ####################################################################################################################
    # COUNTRIES = [(i.alpha_3, i.name) for i in list(pycountry.countries)]  # pycountry.
    # ''' 1)fuzzy_search
    #     2)subdivisions
    #     3)currencies
    #     4)languages
    #     5)locales!!! zaebis
    # '''
    country = models.CharField(
        max_length=255,
        blank=False,
    #   choices=COUNTRIES
    )
    state = models.CharField(
        max_length=255,
        blank=False,
    )
    city = models.CharField(
        max_length=255,
        blank=False,
    )
    street = models.CharField(
        max_length=255,
        blank=False,
    )
    ####################################################################################################################
    WORK_DAYS = [
        ('Sun', 'Sunday'),
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
    ]
    work_days = MultiSelectField(  # https://pypi.org/project/django-multiselectfield/ #### serializer friendly
        blank=False,
        choices=WORK_DAYS,
        max_choices=7
    )
    work_time_start = models.TimeField(
        blank=False
    )
    work_time_end = models.TimeField(
        blank=False
    )

    #################################################################################

    company_rating = models.DecimalField(
        max_digits=2,
        decimal_places=1
    )
    # вычисляемое поле
    '''
    #    select sum(g.grade) from rating r, grade g where
    #    g.id = r.grade_id and
    #    r.company_id = %this%.id
    '''
    #  типо того будет

    website_url = models.URLField(
        max_length=255
    )

    def __str__(self):
        return self.name

    def refresh_rating(self):
        pass

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
#     loyalty_program = models.ForeignKey
#
#
# class LoyaltyProgram:
#     name = models.CharField(
#         max_length=255
#     )
#     description = models.CharField(
#         max_length=565
#     )
#     start_date = models.DateTimeField(default=now())
#     end_date = models.DateTimeField(default='01-01-2999 00:00:00')


class Rating(models.Model):
    GRADES = [
        ('Awful', 1),
        ('Bad', 2),
        ('Satisfying', 3),
        ('Good', 4),
        ('Excellent', 5),
    ]
    grade = models.IntegerField(choices=GRADES)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    def test(self):
        pass

    def test(self):
        pass