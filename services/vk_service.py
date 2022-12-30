from vk_api.vk_api import VkApiMethod, VkApi
from pprint import pprint
from vk_api import VkUserPermissions
from database.database import Database
from database.models.vk_user import VkUser


class VkService:
    API_VERSION = "5.120"
    api: VkApiMethod
    database: Database

    def __init__(self, app_id: int, login: str, password: str, database: Database):
        vk_session = VkApi(login=login, password=password, app_id=app_id, scope=[2 ** 2], api_version=self.API_VERSION)
        vk_session.auth(token_only=True)
        self.api = vk_session.get_api()
        self.database = database

    def get_profile(self):
        response = self.api.account.getProfileInfo()
        return response

    def users_search(self, birth_year: int, city_id: int, gender: int,
                     family_status: int):
        response = self.api.users.search(

            birth_year=birth_year,
            city_id=city_id,
            sex=gender,
            status=family_status,
            count=1000,
            fields=['screen_name']

        )
        return response

    def search_people(self):
        my_profile = self.get_profile()
        gender = my_profile['sex']

        if gender == 1:
            gender = 2
        else:
            gender = 1

        bdate_split = my_profile['bdate'].split('.')
        users = self.users_search(
            gender=gender,
            city_id=my_profile['city']['id'],
            family_status=my_profile['relation'],
            birth_year=int(bdate_split[2])
        )['items']
        users = list(filter(lambda element: element['can_access_closed'], users))
        vk_user: VkUser = None
        for user in users:
            if self.database.is_user_exist(user_id=user['id']):
                continue
            else:
                vk_user = VkUser(
                    id=user['id'],
                    first_name=user['first_name'],
                    last_name=user['last_name'],
                    profile_link=f"https://vk.com/{user['screen_name']}"
                )
                self.database.add_vk_user(vk_user)
                break
        user_photos = self.get_all_photos(user_id=vk_user.id)
        user_top_3_photos = self.get_top_3_photos(user_photos)
        attachments = create_attachment(user_top_3_photos, vk_user.id)
        pprint(user_top_3_photos)
        # pprint(users)
        user_string = convert_user_to_string(vk_user)
        return user_string, attachments

    def get_all_photos(self, user_id: int):
        response = self.api.photos.getAll(owner_id=user_id, extended=1)
        # pprint(response)
        return response['items']

    def get_top_3_photos(self, user_photos: list):
        photos = list(map(convert_user_photo_to_photo, user_photos))
        sorted_photos = sorted(photos, key=lambda photo: photo['like'], reverse=True)
        first_3_photos = sorted_photos[0:3]
        return first_3_photos


def convert_user_to_string(user: VkUser):
    return f"{user.first_name} {user.last_name}\n{user.profile_link}"


def convert_user_photo_to_photo(user_photo):
    return {
        "url": user_photo['sizes'][-1]['url'],
        "like": user_photo['likes']['count'],
        "id": user_photo['id']
    }


def create_attachment(user_photos: list, user_id: int):
    attachments = []
    for photo in user_photos:
        attachment = f"photo{user_id}_{photo['id']}"
        attachments.append(attachment)
    result = ','.join(attachments)
    return result
