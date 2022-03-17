from django.contrib import admin

from .models import Company, Rating, User

admin.site.register(Company)
admin.site.register(Rating)
admin.site.register(User)
