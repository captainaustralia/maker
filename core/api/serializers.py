import requests
from rest_framework import serializers, permissions

from ..models import User, Company


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'phone', 'first_name', 'last_name', 'country', 'city', 'about',
                  'is_active']
        ordering = ['email']


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'

