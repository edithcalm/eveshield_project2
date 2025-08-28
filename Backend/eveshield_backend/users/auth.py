from django.shortcuts import render
from rest_framework import serializers
from .serializers import RegisterUserSerializer, LoginUserSerializer, UserSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model


# authentication & Permisions api views

User = get_user_model()


class RegisterUserAPIView(GenericAPIView):
    """
    An endpoint for the client to create a new User.
    """

    permission_classes = (AllowAny,)
    serializer_class = RegisterUserSerializer

    def get(self, request):
        return Response(
            {
                'message': 'Use POST request with phone_number & password to register new user'
            },
            status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        token = RefreshToken.for_user(user)

        data = serializer.data

        data["tokens"] = {"refresh": str(
            token), "access": str(token.access_token)}

        return Response(data, status=status.HTTP_201_CREATED)


class LoginUserAPIView(GenericAPIView):
    """
    An endpoint to authenticate existing users using their phone_number and password.
    """

    permission_classes = (AllowAny,)
    serializer_class = LoginUserSerializer

    def get(self, request):
        return Response(
            {
                "message": "Use POST request with phone_number & password to login user"
            },
            status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data

        serializer = UserSerializer(user)

        token = RefreshToken.for_user(user)

        data = serializer.data

        data["tokens"] = {"refresh": str(
            token), "access": str(token.access_token)}

        return Response(data, status=status.HTTP_200_OK)


class LogoutUserAPIView(GenericAPIView):
    """
    An endpoint to logout users.
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
