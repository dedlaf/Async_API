import http
import json
from enum import StrEnum, auto

import requests
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from pydantic import BaseModel


User = get_user_model()

class Roles(StrEnum):
    ADMIN = auto()
    SUBSCRIBER = auto()

class UserLoginSchema(BaseModel):
    username: str
    password: str

class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        url = settings.AUTH_API_LOGIN_URL
        payload = {'username': str(username), 'password': str(password)}
        response = requests.post(url, json=payload)
        if response.status_code != http.HTTPStatus.OK:
            return None
        user_data = response.json()
        payload_role = {
            'id': user_data['role_id'],
        }
        print('now1', response.json(), payload_role)
        response_role = requests.get(settings.AUTH_API_ROLE_URL+"/"+payload_role.get('id'),)
        print('now2', response_role.json())
        user_role_data = response_role.json()
        try:
            print('start')
            user, created = User.objects.get_or_create(email=user_data['email'], )
            print('now3', user, created)
            user.email = user_data.get('email')
            user.first_name = user_data.get('first_name', "")
            user.last_name = user_data.get('last_name', "")
            user.is_admin = user_role_data.get('name') == Roles.ADMIN

            user.is_staff = True
            user.is_active = user_data.get('is_active', True)
            user.save()
        except Exception:
            return None

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
