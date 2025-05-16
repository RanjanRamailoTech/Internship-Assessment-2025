from user.models.user import User
from user.serializers.user_serializer import UserSerializer
from user.services.email_service import EmailService
from user.error_handling import BrokerConnectionError, ValidationError
from kombu.exceptions import OperationalError
import redis
from user.error_handling import DuplicateEmailError

class UserService:
    @staticmethod
    def create_user(data, request):
        serializer = UserSerializer(data=data)
        if not serializer.is_valid():
            error_field = next(iter(serializer.errors))
            error_message = serializer.errors[error_field][0]
            raise ValidationError(message=error_message, param=error_field)
        email = serializer.validated_data["email"]
        if User.objects.filter(email=email).exists():
            raise DuplicateEmailError()
        
        user, created = User.get_or_create_user(email=email)
        if created:
            user.name = serializer.validated_data.get("name", "")
            user.save()
            try:
                EmailService.send_verification_email(user, request)
            except (redis.exceptions.ConnectionError, OperationalError):
                raise BrokerConnectionError()
        return user, created