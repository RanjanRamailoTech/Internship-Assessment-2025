from django.conf import settings
from django.template.loader import render_to_string
from user.models.user import User
from user.services.auth_service import AuthService
from user.tasks.email_tasks import send_email
from django.urls import reverse
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import TokenError


class EmailService:
    @staticmethod
    def send_verification_email(user, request):
        token = AuthService.generate_token(user)["access"]
        verification_link = request.build_absolute_uri(
            reverse("verifyemail")
        )
        receiver = [user.email]
        template = "email_verification_link_template.html"

        subject = "Verify Your Email Address"
        body = render_to_string(template, {
            "name": user.name or "User",
            "link": verification_link,
            "expiry": int(settings.EMAIL_LINK_EXPIRY / 60) if hasattr(settings, 'EMAIL_LINK_EXPIRY') else 30,
        })
        send_email.delay(subject, body, receiver)

    @staticmethod
    def verify_email(token):
        try:
            UntypedToken(token)  # Validate the token
            user_id = UntypedToken(token).payload.get("id")
            user = User.objects.get(id=user_id)
            if not user.is_email_verified:
                user.is_email_verified = True
                user.save()
            return True, "Email verified successfully"
        except (TokenError, User.DoesNotExist):
            return False, "Invalid or expired token"