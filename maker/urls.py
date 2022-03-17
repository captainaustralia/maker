from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin default
    path('api/v1/', include('core.urls')),  # API interface
    path('auth/', include('djoser.urls.jwt')),  # create token - auth , refresh, verify
    path('test/', include('djoser.urls'))  # reset pass/ reset email/ activate/ change pass/ change email
]
