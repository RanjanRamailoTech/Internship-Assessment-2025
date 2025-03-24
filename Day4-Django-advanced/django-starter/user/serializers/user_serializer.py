from rest_framework import serializers
from user.models.user import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.validators import MinLengthValidator

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,)
    name = serializers.CharField(
        required=True,
        allow_blank=False,
        validators=[MinLengthValidator(3, message="Name must be at least 3 characters long.")]
    )

    class Meta:
        model = User
        fields = ["name", "email"]

class UserLoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        return data

class RefreshTokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()