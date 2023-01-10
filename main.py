from dotenv import load_dotenv
import os
from services.vk_service import VkService
from services.vk_bot_service import VkBotService
from vk_api.bot_longpoll import VkBotEventType
from database.database import Database


def main():
    load_dotenv()

    token = os.getenv('BOT_SECRET_TOKEN')
    app_id = int(os.getenv('VK_APP_ID'))
    login = os.getenv('VK_LOGIN')
    password = os.getenv('VK_PASSWORD')
    group_id = os.getenv('VK_GROUP_ID')
    database_link = os.getenv('DATABASE_LINK')

    database = Database(database_link=database_link)

    vk_service = VkService(app_id=app_id, login=login, password=password, database=database)
    vk_bot_service = VkBotService(token=token, group_id=group_id)

    for event in vk_bot_service.long_poll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            print(f'New message: {event.obj.message["text"]}')
            if event.from_user:
                user_text = event.obj.message["text"]

                if user_text == 'найти':
                    vk_bot_service.send_message(user_id=event.obj.message['from_id'], message='Ок, начинаем поиск...')
                    result_message = vk_service.search_people()

                    if result_message:

                        vk_bot_service.send_message(user_id=event.obj.message['from_id'], message=result_message[0],
                                                attachments=result_message[1])

            else:
                pass


if __name__ == '__main__':
    main()
