from rest_framework_simplejwt.tokens import RefreshToken
from user.serializers.user_serializer import RefreshTokenSerializer


class AuthService:
    @staticmethod
    def generate_token(user):
        refresh = RefreshToken.for_user(user)
        serializer = RefreshTokenSerializer({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })
        return serializer.data