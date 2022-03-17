from django.contrib import admin

from .models import CompanyProfile, Rating, User

admin.site.register(CompanyProfile)
admin.site.register(Rating)
admin.site.register(User)
