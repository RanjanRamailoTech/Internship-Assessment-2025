from user.models.user import User
from user.serializers.user_serializer import UserSerializer
from user.services.email_service import EmailService


class UserService:
    @staticmethod
    def create_user(data, request):
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user, created = User.get_or_create_user(email=data["email"])
            if created:
                user.name = data.get("name", "")
                user.save()
                EmailService.send_verification_email(user, request)
            return user, created
        return None, serializer.errors