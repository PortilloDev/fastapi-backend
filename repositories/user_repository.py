# repositories/user_repository.py
from models.user import User

user_list = []

class UserRepository:

    @staticmethod
    def get_all_users():
        return user_list

    @staticmethod
    def get_user_by_id(user_id: int):
        user = filter(lambda u: u.id == user_id, user_list)
        try:
            return list(user)[0]
        except IndexError:
            return None

    @staticmethod
    def add_user(user: User):
        user_list.append(user)
        return user

    @staticmethod
    def delete_user(user_id: int):
        user = UserRepository.get_user_by_id(user_id)
        if user:
            user_list.remove(user)
        return user