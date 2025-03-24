from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(BaseModel):
    name = models.CharField(max_length=255, blank=False)
    email = models.CharField(max_length=128, unique=True, blank=False)
    is_email_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.email}"


    @property
    def is_verified(self):
        return self.is_email_verified

    @classmethod
    def get_or_create_user(cls, email):
        user, created = cls.objects.get_or_create(email=email)
        return user, created