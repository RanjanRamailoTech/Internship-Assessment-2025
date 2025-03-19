from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def get_all_users(cls):
        return cls.objects.all()

    @classmethod
    def get_user_by_id(cls, user_id):
        try:
            return cls.objects.get(pk=user_id)
        except cls.DoesNotExist:
            return None

    @classmethod
    def create_user(cls, first_name, last_name, email):
        return cls.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email
        )

    @classmethod
    def update_user(cls, user_id, first_name=None, last_name=None, email=None):
        user = cls.get_user_by_id(user_id)
        if not user:
            return None
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if email is not None:
            user.email = email
        user.save()
        return user

    @classmethod
    def delete_user(cls, user_id):
        user = cls.get_user_by_id(user_id)
        if not user:
            return False
        user.delete()
        return True