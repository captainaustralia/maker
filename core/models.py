from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.db import models
from multiselectfield import MultiSelectField
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.timezone import now


class UserManager(BaseUserManager):
    def create_user(self, email, phone, country, city, password, is_staff=False, is_admin=False, is_active=False,
                    is_company=False):
        user_obj = self.model(
            email=self.normalize_email(email)
        )
        user_obj.phone = phone
        user_obj.country = country
        user_obj.city = city
        user_obj.is_staff = is_staff
        user_obj.is_admin = is_admin
        user_obj.is_active = is_active
        user_obj.is_company = is_company
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, email, password, phone='', country='', city=''):
        user = self.create_user(
            email,
            password=password,
            phone=phone,
            country=country,
            city=city,
            is_staff=True,
            is_admin=True,
            is_active=True,
        )
        return user

    # def create_company(self, email, password, phone='', country='', city=''):
    #     company = self.create_user(
    #         email,
    #         password=password,
    #         phone=phone,
    #         country=country,
    #         city=city,
    #         is_company=True
    #     )
    #     return company


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False
    )

    username = models.CharField(
        max_length=255,
        editable=True,
        unique=True
    )

    is_active = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)

    is_company = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['phone', 'country', 'city']

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


# class UserProfile(models.Model):
#     user = models.OneToOneField(
#         User,
#         on_delete=models.PROTECT,
#         null=True,
#         default=''
#     )
#
#     # about = models.TextField(
#     #     max_length=200,
#     #     blank=True
#     # )


class Company(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT
    )
    avatar = models.ImageField(
        upload_to='media/user_avatar'
    )
    name = models.CharField(
        max_length=255,
        editable=True,
        unique=True
    )

    description = models.CharField(
        max_length=1155
    )

    phone = PhoneNumberField()
    start_date = models.DateTimeField(default=now())
    end_date = models.DateTimeField()  # not sure about format

    country = models.CharField(
        max_length=255
    )
    city = models.CharField(
        max_length=255
    )
    state = models.CharField(
        max_length=255
    )
    street = models.CharField(
        max_length=255
    )
    WORK_DAYS = [
        ('Sun', 'Sunday'),
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
    ]
    work_days = MultiSelectField(
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
    company_rating = models.DecimalField(
        max_digits=2,
        decimal_places=1
    )
    website_url = models.URLField(
        max_length=255
    )

    likes = models.IntegerField()
    dislikes = models.IntegerField()

    def __str__(self):
        return self.user.name

    def save(self, *args, **kwargs):
        self.objects.create_user(*args, **kwargs)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class Category(models.Model):
    name = models.CharField(
        max_length=255
    )

