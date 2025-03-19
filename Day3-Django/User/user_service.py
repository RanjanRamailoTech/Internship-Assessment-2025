from .models import User

class UserService:
    @staticmethod
    def get_all_users():
        return User.get_all_users()

    @staticmethod
    def get_user_by_id(user_id):
        return User.get_user_by_id(user_id)

    @staticmethod
    def create_user(first_name, last_name, email):
        return User.create_user(first_name, last_name, email)

    @staticmethod
    def update_user(user_id, first_name=None, last_name=None, email=None):
        return User.update_user(user_id, first_name=first_name, last_name=last_name, email=email)

    @staticmethod
    def delete_user(user_id):
        return User.delete_user(user_id)
