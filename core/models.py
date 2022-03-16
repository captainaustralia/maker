import django.db.models.base
import pycountry
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from multiselectfield import MultiSelectField
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_staff=False, is_admin=False, active=True): ####убрать пас=нон
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
    COUNTRIES = [(i.alpha_3, i.name) for i in list(pycountry.countries)]  # pycountry.
    ''' 1)fuzzy_search
        2)subdivisions
        3)currencies
        4)languages
    '''
    country = models.CharField(
        max_length=255,
        blank=False,
        choices=COUNTRIES
    )

    city = models.CharField(
        max_length=30,
        blank=False
    )
    """Maybe worth create table 'Location' idk, but now we can send ajax to API postman or other"""
    """???"""
    """Also maybe need postpone about/first_name/last_name in profile"""
    """2 step register, 1 - email/pass/phone/city , 2 - profile info: firstname/lastname/about/avatar"""
    about = models.TextField(  # маленькая длина
        max_length=200,
        blank=True
    )
    """Field for write about info"""
    user_confirm = models.BooleanField(  # is_confirmed
        default=False
    )
    """After registration, we will send a confirmation link to mail, after confirmation, the flag will be changed"""

    active = models.BooleanField(default=True)                  ################добавить is_ + default=false before confirmation
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
    ####################################################################################################################
    COUNTRIES = [(i.alpha_3, i.name) for i in list(pycountry.countries)]  # pycountry.
    ''' 1)fuzzy_search
        2)subdivisions
        3)currencies
        4)languages
        5)locales!!! zaebis
    '''
    country = models.CharField(
        # https://www.back4app.com/database/back4app/list-of-all-continents-countries-cities/graphql-playground/all-countries
        max_length=255,
        blank=False,
        choices=COUNTRIES
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
        max_length=255,
        blank=False,
        choices=WORK_DAYS,
        max_choices=7
    )
    work_time_start_hh = models.TimeField(

    )
    work_time_start_mm = models.TimeField(

    )
    work_time_end_hh = models.TimeField(

    )
    work_time_end_mm = models.TimeField(

    )
    #################################################################################

    rating = models.DecimalField(
        # вычисляемое поле
        '''
        #    select sum(g.grade) from rating r, grade g where
        #    g.id = r.grade_id and
        #    r.company_id = %this%.id
        '''
        #  типо того будет
    )

    website_url = models.URLField(

    )


class Grade:  # 1,2,3,4,5
    title = models.CharField(
        max_length=55
    )
    grade = models.IntegerField(

    )


class Rating:   # m2m
    grade = models.ForeignKey(Grade)
    company = models.ForeignKey(Company)

