from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.custom_exception import InternalServerException

from .serializers import UserSerializer
from user import serializers
from django.db.models import Q
from .models import User


# Create your views here.


class RegisterUser(APIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'user_name': user.user_name
        })


class LogIn(APIView):
    def get(self, request, *args, **kwargs):
        user_name_or_email = request.data.get('user_name_or_email', None)
        if not user_name_or_email:
            raise InternalServerException(500, 'user_name_or_email field is required')

        try:
            user = User.objects.get(Q(email=user_name_or_email) | Q(user_name=user_name_or_email))
        except User.DoesNotExist:
            raise InternalServerException(500, f'User does not exists for user name or email {user_name_or_email}')

        if not user:
            raise InternalServerException(500, f'User does not exists for user name or email {user_name_or_email}')

        token = Token.objects.get(user=user)

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'user_name': user.user_name
        })
