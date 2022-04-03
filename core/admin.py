from django.contrib import admin

from .models import Company, User, Category, MediaCompanyStorage, MediaUserStorage

admin.site.register(Company)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(MediaCompanyStorage)
admin.site.register(MediaUserStorage)
