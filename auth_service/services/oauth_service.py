from .vk_oauth_service import VkOauth
from .yandex_oauth_service import YandexOauth


class OauthService:
    def __init__(self):
        self.vk = VkOauth()
        self.yandex = YandexOauth()

    def get_authorization_url(self, service):
        if service == 'vk':
            authorization_url = self.vk.get_vk_auth_url()
            return authorization_url
        elif service == 'yandex':
            authorization_url = self.yandex.get_yandex_auth_url()
            return authorization_url

    async def get_user(self, service, code, device_id: str = None, state: str = None):
        if service == 'vk':
            user_info = await self.vk.get_vk_user(code=code, device_id=device_id, state=state)
            return user_info
        elif service == 'yandex':
            user_info = await self.yandex.get_yandex_user(code=code)
            return user_info


def get_oauth_service():
    return OauthService()