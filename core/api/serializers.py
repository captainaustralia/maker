import requests
from rest_framework import serializers, permissions

from ..models import User, Company


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']
        ordering = ['email']


class CompanySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Company
        fields = '__all__'

