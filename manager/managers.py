from unittest.mock import Base
from django.contrib.auth.base_user import BaseUserManager
import string
import random


class WorkerManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)

        if not extra_fields.get("username"):
            extra_fields["username"] = self.generate_random_username()

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

    def generate_random_username(self, length=10):
        return "user_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))