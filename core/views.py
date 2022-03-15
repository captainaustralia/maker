from django.shortcuts import render
from rest_framework import generics, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from core.api.serializers import UserSerializer
from core.models import User


class UserViewSet(viewsets.ModelViewSet):
    """
    UserApi
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]