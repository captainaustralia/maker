from rest_framework import serializers

from ..models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'phone', 'first_name', 'last_name', 'country', 'city', 'about',
                  'is_active']
        ordering = ['email']

