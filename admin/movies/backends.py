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
        print("connecting", payload, username, password)
        response = requests.post(url, json=payload)
        print(response.status_code, response.text)
        if response.status_code != http.HTTPStatus.OK:
            return None

        data = response.json()

        try:
            user, created = User.objects.get_or_create(email=data['email'], )
            print(user, created)
            user.email = data.get('email')
            user.first_name = data.get('first_name', "")
            user.last_name = data.get('last_name', "")
            # user.is_admin = data.get('role') == Roles.ADMIN
            #user.is_admin = data.get('role') == "admin"
            user.is_admin = True
            user.is_staff = True
            user.is_active = data.get('is_active', True)
            user.save()
        except Exception:
            print("error")
            return None

        print("done", user)
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
