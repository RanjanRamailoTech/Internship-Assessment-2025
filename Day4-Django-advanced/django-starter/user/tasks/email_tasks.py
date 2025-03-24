from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage


@shared_task(name="send_email")
def send_email(subject: str, body: str, receiver: list, attachment=None):
    sender = f"{settings.COMPANY_NAME} <{settings.EMAIL_HOST_USER}>"
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=sender,
        to=receiver,
    )
    if attachment:
        email.attach(**attachment)
    email.content_subtype = 'html'
    email.send(fail_silently=False)