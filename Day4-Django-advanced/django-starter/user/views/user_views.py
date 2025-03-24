from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from user.serializers.user_serializer import RefreshTokenSerializer, UserSerializer, UserLoginSerializer
from user.services.user_service import UserService
from user.services.auth_service import AuthService
from user.services.email_service import EmailService
from ramailo.builders.response_builder import ResponseBuilder
from user.openapi.schema import CREATE_USER_API, LOGIN_API, VERIFY_EMAIL_API

class CreateUserView(APIView):
    @swagger_auto_schema(**CREATE_USER_API)
    def post(self, request):
        user, result = UserService.create_user(request.data, request)
        if isinstance(result, bool):
            return ResponseBuilder().success().created_201().result_object(UserSerializer(user).data).get_response()
        return ResponseBuilder().fail().bad_request_400().result_object(result).get_response()

class LoginView(APIView):
    @swagger_auto_schema(**LOGIN_API)
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            tokens = AuthService.generate_token(user)
            return ResponseBuilder().success().ok_200().result_object(tokens).get_response()
        return ResponseBuilder().fail().user_unauthorized_401().result_object(serializer.errors).get_response()

class VerifyEmailView(APIView):
    @swagger_auto_schema(**VERIFY_EMAIL_API)
    def get(self, request, token):
        success, message = EmailService.verify_email(token)
        if success:
            return ResponseBuilder().success().ok_200().message(message).get_response()
        return ResponseBuilder().fail().bad_request_400().message(message).get_response()