from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from user.serializers.user_serializer import RefreshTokenSerializer, UserSerializer, UserLoginSerializer
from user.services.user_service import UserService
from user.services.auth_service import AuthService
from user.services.email_service import EmailService


class CreateUserView(APIView):
    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={201: UserSerializer, 400: "Bad Request"},
        operation_description="Create a new user and send email verification link."
    )
    def post(self, request):
        user, result = UserService.create_user(request.data, request)
        if isinstance(result, bool):  # Success
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(result, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={200: RefreshTokenSerializer, 401: "Unauthorized"},
        operation_description="Log in a user and return JWT tokens."
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            tokens = AuthService.generate_token(user)
            return Response(tokens, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class VerifyEmailView(APIView):
    @swagger_auto_schema(
        responses={200: "Email verified", 400: "Invalid token"},
        operation_description="Verify user email using the provided token."
    )
    def get(self, request, token):
        success, message = EmailService.verify_email(token)
        if success:
            return Response({"message": message}, status=status.HTTP_200_OK)
        return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)