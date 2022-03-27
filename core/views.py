import datetime

from django.dispatch import Signal
from django.shortcuts import render
from rest_framework import generics, viewsets, permissions, status, authentication
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.permissions import IsOwnerOrReadOnly
from core.api.serializers import UserSerializer, CompanySerializer
from core.models import User, Company


class UserViewSet(viewsets.ModelViewSet):
    """
    UserApi
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class CompanyListAPIView(generics.ListAPIView):
    """
    LIST COMPANIES
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]


class CompanyUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET/UPDATE/DELETE
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (IsOwnerOrReadOnly,)


class CompanyCreateAPIView(APIView):
    """
    Companies Create API
    """

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # If someone wants to bypass the interface to someone else's user ID, he will not be able to create a company
    # + he must be auth... Need more test's
    def post(self, request):
        data = request.data
        serializer = CompanySerializer(data=data)
        if serializer.is_valid() and str(serializer.validated_data.get('user')) == str(request.user.username):
            user = User.objects.get(username=request.user.username)
            serializer.save()
            user.is_company = True
            user.save()
            create_company = Signal()
            create_company.send(sender=self.__class__, id=request.user.username)
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # send 201
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # send 400


class SelectedCategoryCompanies(APIView):
    """
    Selected Category Companies
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, category, city, day=str(datetime.date.isoweekday(datetime.date.today())),
            time=datetime.datetime.today().time()):
        queryset = Company.objects.filter(category__name=category,
                                          city=city.title(), work_time_end__hour__gt=time.hour,
                                          work_days__icontains=str(day))
        serializer = CompanySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


def test(request):
    return render(request, 'login.html')

