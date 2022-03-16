from django.contrib import admin

from .models import Company, Rating

admin.site.register(Company)
admin.site.register(Rating)