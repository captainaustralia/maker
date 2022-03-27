from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.db import models
from multiselectfield import MultiSelectField
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_staff=False, is_admin=False, is_active=False,
                    is_company=False, **kwargs):
        user_obj = self.model(
            email=self.normalize_email(email)
        )
        user_obj.username = email
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
            password=password,
            is_staff=True,
            is_admin=True,
            is_active=True,
        )
        return user


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
    # date_register = models.DateTimeField(default='2021-12-12 23:59:59.880291')

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
        blank=False,
        null=True,
        related_name='category',
        on_delete=models.SET_NULL,
    )

    name = models.CharField(
        max_length=255,
        editable=True,
        unique=True
    )
    avatar = models.ImageField(
        upload_to=f'media/user_avatar/{name}/',  # Amazon storage in future - Done!
        default='media/user_avatar/default.png',
        blank=True,
    )

    description = models.CharField(
        max_length=1155
    )

    phone = PhoneNumberField(
        blank=False
    )

    start_date = models.DateTimeField(
        auto_now_add=True
    )

    end_date = models.DateTimeField(
        blank=False
    )

    country = models.CharField(
        max_length=255,
        blank=False
    )
    city = models.CharField(
        max_length=255,
        blank=False
    )
    state = models.CharField(
        max_length=255,
        blank=False
    )
    street = models.CharField(
        max_length=255,
        blank=False
    )

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
        return f'{self.name},{self.user.email}'

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class MediaStorage(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    link = models.FileField()
    date = models.DateTimeField(auto_now_add=True)


class UserStorage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    link = models.FileField()
    date = models.DateTimeField(auto_now_add=True)
