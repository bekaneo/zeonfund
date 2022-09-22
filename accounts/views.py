from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.serializers import (ProfileSerializer,
                                  RegistrationSerializer,
                                  LoginSerializer,
                                  RestorePasswordSerializer,
                                  RestorePasswordCompleteSerializer,
                                  ChangePasswordSerializer,
                                  UsersListSerializer)

User = get_user_model()


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UsersListSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email']


class ProfileView(ListAPIView):
    serializer_class = ProfileSerializer

    def list(self, request, email, *args, **kwargs):
        queryset = User.objects.filter(email=email)
        serializer = ProfileSerializer(queryset, context={'request': request}, many=True)

        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('User not found', status=status.HTTP_404_NOT_FOUND)


class RegistrationView(APIView):
    @swagger_auto_schema(request_body=RegistrationSerializer)
    def post(self, request):
        data = request.data
        serializer = RegistrationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.create()
            return Response('Successfully created', status=status.HTTP_201_CREATED)


class ActivationView(APIView):
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response('Account is activated', status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response('Activation code is invalid', status=status.HTTP_404_NOT_FOUND)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class UpdateTokenView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.data.get('refresh_token')

        if token is not None:
            token_object = RefreshToken(token)
            token_object.blacklist()
            return Response('Logout successfully')

        return Response('There is no token', status=status.HTTP_400_BAD_REQUEST)


class RestorePasswordView(APIView):
    @swagger_auto_schema(request_body=RestorePasswordSerializer)
    def post(self, request):
        data = request.data
        serializer = RestorePasswordSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_verification_code()
            return Response('Check your email for code', status=status.HTTP_201_CREATED)


class RestorePasswordCompleteView(APIView):
    @swagger_auto_schema(request_body=RestorePasswordCompleteSerializer)
    def post(self, request):
        data = request.data
        serializer = RestorePasswordCompleteSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response('Password is successfully updated', status=status.HTTP_201_CREATED)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def post(self, request):
        data = request.data
        serializer = ChangePasswordSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('Password is successfully updated', status=status.HTTP_201_CREATED)
