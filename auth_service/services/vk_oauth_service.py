import base64
import random
import string

import aiohttp
from core.config.components.settings import settings
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


class VkOauth:
    def __init__(self):
        self.client_id = settings.vk_client_id
        self.client_secret = settings.vk_client_secret
        self.code_verifier = settings.vk_code_verifier
        self.redirect_uri = settings.vk_redirect_uri

    @staticmethod
    def _generate_random_state(length=32):
        characters = string.ascii_letters + string.digits + '_-'
        state = ''.join(random.choice(characters) for _ in range(length))
        return state

    @staticmethod
    def _generate_code_challenge(code_verifier):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(code_verifier.encode('utf-8'))
        code_challenge_hash = digest.finalize()

        code_challenge = base64.urlsafe_b64encode(code_challenge_hash).rstrip(b'=').decode('utf-8')

        return code_challenge

    @staticmethod
    async def _get_vk_access_token(vk_access_data):
        async with aiohttp.ClientSession() as session:
            async with session.post("https://id.vk.com/oauth2/auth", data=vk_access_data) as response:
                vk_access_token = await response.json()

            return vk_access_token.get('access_token')

    def _get_vk_access_data(self, code: str, device_id: str, state: str):
        vk_access_data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code_verifier": self.code_verifier,
            "device_id": device_id,
            "redirect_uri": self.redirect_uri,
            "state": state
        }
        return vk_access_data

    async def _get_vk_user_info(self, access_token):
        data_for_user_info = {"access_token": access_token, "client_id": self.client_id}
        async with aiohttp.ClientSession() as session:
            async with session.post("https://id.vk.com/oauth2/user_info", data=data_for_user_info) as response:
                user_info = await response.json()

                return user_info

    def _get_vk_auth_query(self):
        state = self._generate_random_state()
        code_challenge = self._generate_code_challenge(self.code_verifier)
        query = f"?response_type=code" \
            f"&client_id={self.client_id}" \
            f"&redirect_uri={self.redirect_uri}" \
            f"&state={state}" \
            f"&code_challenge={code_challenge}" \
            f"&code_challenge_method=s256"
        return query

    async def get_vk_user(self, device_id, state, code):
        vk_access_data = self._get_vk_access_data(device_id=device_id, state=state, code=code)
        access_token = await self._get_vk_access_token(vk_access_data)
        user_info = await self._get_vk_user_info(access_token)

        return user_info

    def get_vk_auth_url(self):
        query = self._get_vk_auth_query()
        authorization_url = f"https://id.vk.com/authorize{query}"

        return authorization_url
