from django.shortcuts import render
from rest_framework import serializers
from .serializers import RegisterUserSerializer, LoginUserSerializer, UserSerializer, PasswordResetSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
