from vk_api import VkApi
from vk_api.keyboard import VkKeyboard
from vk_api.bot_longpoll import VkBotLongPoll
from random import randrange


class VkBotService:
    vk_api: VkApi
    long_poll: VkBotLongPoll

    def __init__(self, token: str, group_id: str):
        self.vk_api = VkApi(token=token, api_version='5.131')
        self.long_poll = VkBotLongPoll(self.vk_api, group_id=group_id)

    def send_message(self, user_id: int, message: str, attachments: str = None):
        self.vk_api.method(
            'messages.send',
            {
                'user_id': user_id,
                'message': message,
                'random_id': randrange(10 ** 7),
                'attachment': attachments
            }
        )

    def show_keyboard(self, user_id: int, keyboard: VkKeyboard, peer_id):
        self.vk_api.method(
            'messages.send',
            {
                'user_id': user_id,
                'random_id': randrange(10 ** 7),
                'keyboard': keyboard.get_keyboard(),
                'message': 'Нажмите на кнопку',
                'peer_id': peer_id
            }
        )
