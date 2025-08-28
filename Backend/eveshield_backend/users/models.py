from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.core.validators import RegexValidator
import uuid


# User

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, username, email=None, password=None, **extra_fields):
        """Create and return a regular user with phone_number instead of username or email."""
        if not phone_number:
            raise ValueError("Phone number is required")

        email = self.normalize_email(email)

        user = self.model(
            phone_number=phone_number,
            username=username,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, username, email=None, password=None, **extra_fields):
        """Create and return a superuser."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if not password:
            raise ValueError("Superusers must have a password.")

        return self.create_user(phone_number, username, email, password, **extra_fields)

    def normalize_phone_number(self, phone_number):
        # Normalize e.g. 0712345678 -> +254712345678
        if phone_number.startswith('0') and len(phone_number) == 10:
            return '+254' + phone_number[1:]
        return phone_number


class CustomUser(AbstractUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    phone_regex = RegexValidator(
        regex=r'^\+?254\d{9}$',
        message="Phone number must be in the format: '+2547XXXXXXXX'"
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=15,
        unique=True
    )

    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(unique=False, blank=True,
                              null=True)  # Ensure email is unique, but can also be blank
    username = models.CharField(max_length=50, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'  # Set phone_number as the primary identifier
    REQUIRED_FIELDS = ['username']  # username is a required field

    def __str__(self):
        return self.phone_number


class EmergencyContact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="emergency_contacts")
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    relationship = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.relationship})"
