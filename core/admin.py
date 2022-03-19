from django.contrib import admin

from .models import Company, User, Category

admin.site.register(Company)
admin.site.register(User)
admin.site.register(Category)