from .vk_oauth_service import VkOauth
from .yandex_oauth_service import YandexOauth


class OauthService:
    def __init__(self):
        self.vk = VkOauth()
        self.yandex = YandexOauth()

    def get_authorization_url_yandex(self):
        authorization_url = self.yandex.get_yandex_auth_url()
        return authorization_url

    def get_authorization_url_vk(self):
        authorization_url = self.vk.get_vk_auth_url()
        return authorization_url

    async def get_user_yandex(self, code):
        user_info = await self.yandex.get_yandex_user(code=code)
        return user_info

    async def get_user_vk(self, code, device_id: str = None, state: str = None):
        user_info = await self.vk.get_vk_user(
            code=code, device_id=device_id, state=state
        )
        return user_info


def get_oauth_service():
    return OauthService()
