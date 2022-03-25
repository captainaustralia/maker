from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.db import models
from multiselectfield import MultiSelectField
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.timezone import now


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, username='', is_staff=False, is_admin=False, is_active=False,
                    is_company=False):
        user_obj = self.model(
            email=self.normalize_email(email)
        )
        user_obj.username = username
        user_obj.is_staff = is_staff
        user_obj.is_admin = is_admin
        user_obj.is_active = is_active
        user_obj.is_company = is_company
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            username='',
            password=password,
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
        unique=True,
        blank=True
    )
    date_register = models.DateTimeField(default='2021-12-12 23:59:59.880291')

    is_active = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)

    is_company = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

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

class Category(models.Model):
    name = models.CharField(
        max_length=255
    )

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Company(models.Model):
    WORK_DAYS = [
        ('1', 'Sunday'),
        ('2', 'Monday'),
        ('3', 'Tuesday'),
        ('4', 'Wednesday'),
        ('5', 'Thursday'),
        ('6', 'Friday'),
        ('7', 'Saturday'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT
    )

    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        related_name='category',
        on_delete=models.SET_NULL,
    )
    avatar = models.ImageField(
        upload_to='media/user_avatar',
        blank=True
    )
    name = models.CharField(
        max_length=255,
        editable=True,
        unique=True
    )

    description = models.CharField(
        max_length=1155
    )

    phone = PhoneNumberField(
        unique=True
    )

    start_date = models.DateTimeField(
        auto_now_add=True
    )

    end_date = models.DateTimeField(
        default='2023-12-12 23:59:59'
    )  # not sure about format

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

    work_days = MultiSelectField(
        blank=True,
        choices=WORK_DAYS,
        max_choices=7
    )

    work_time_start = models.TimeField(
        auto_now_add=True
    )

    work_time_end = models.TimeField(
        blank=True
    )

    website_url = models.URLField(
        max_length=255,
        blank=True
    )

    likes = models.IntegerField(
        default=0
    )

    dislikes = models.IntegerField(
        default=0
    )

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
