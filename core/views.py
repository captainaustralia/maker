from django.dispatch import Signal
from rest_framework import generics, viewsets, permissions, status, authentication
from rest_framework.response import Response
from rest_framework.views import APIView
from core.api.serializers import UserSerializer, CompanySerializer
from core.models import User, Company


class UserViewSet(viewsets.ModelViewSet):
    """
    UserApi
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CompanyListAPIView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


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
            print('GG')
            user = User.objects.get(username=request.user.username)
            serializer.save()
            user.is_company = True
            user.save()
            create_company = Signal()
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # send 201
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # send 400
