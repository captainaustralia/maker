from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet, CompanyCreateAPIView, CompanyListAPIView, SelectedCategoryCompanies, \
    CompanyUpdateAPIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.SimpleRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # get token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # refresh token
    path('company/', CompanyCreateAPIView.as_view()),  # create company
    path('company_list/', CompanyListAPIView.as_view()),  # list companies
    path('company_list/<str:category>/<str:city>', SelectedCategoryCompanies.as_view()),  # current city/category comp
    path('company_update/<int:pk>', CompanyUpdateAPIView.as_view()),  # RUD comp (Profile)
]
