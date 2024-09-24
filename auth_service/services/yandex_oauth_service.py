import aiohttp
from core.config.components.settings import settings


class YandexOauth:
    def __init__(self):
        self.client_id = settings.yandex_client_id
        self.client_secret = settings.yandex_client_secret

    def _get_yandex_query(self):
        query = f"?response_type=code" f"&client_id={self.client_id}"
        return query

    def _get_yandex_access_data(self, code):
        yandex_access_data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        return yandex_access_data

    @staticmethod
    async def _get_yandex_access_token(yandex_access_data):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://oauth.yandex.ru/token", data=yandex_access_data
            ) as response:
                yandex_access_token = await response.json()

                return yandex_access_token.get("access_token")

    @staticmethod
    async def _get_yandex_user_info(yandex_access_token):
        yandex_user_info_headers = {"Authorization": f"OAuth {yandex_access_token}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://login.yandex.ru/info?format=json",
                headers=yandex_user_info_headers,
            ) as response:
                yandex_user_info_response = await response.json()

                return yandex_user_info_response

    async def get_yandex_user(self, code):
        yandex_access_data = self._get_yandex_access_data(code)
        access_token = await self._get_yandex_access_token(yandex_access_data)
        user_info = await self._get_yandex_user_info(access_token)

        return user_info

    def get_yandex_auth_url(self):
        query = self._get_yandex_query()
        authorization_url = f"https://oauth.yandex.ru/authorize{query}"
        return authorization_url
