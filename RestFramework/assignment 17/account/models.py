from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.utils.html import mark_safe
from django.utils import timezone
from datetime import timedelta
import hashlib

# Phone validator
phone_validator = RegexValidator(
    r"^(\+?\d{0,4})?\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{4}\)?)?$",
    "The phone number provided is invalid"
)

# User Manager
class Manager(BaseUserManager):
    def create_user(self, username, email, phone, password=None, **extra_fields):
        if not username or not email or not phone:
            raise ValueError("Username and Email and Phone are required")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, phone=phone, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self.create_user(username, email, phone, password, **extra_fields)

# Custom User
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True, validators=[UnicodeUsernameValidator()])
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True, validators=[phone_validator])

    image = models.ImageField(upload_to="users/", default="defaults/default.jpg")
    country = models.CharField(max_length=150, blank=True, null=True, db_index=True)
    city = models.CharField(max_length=150, blank=True, null=True, db_index=True)
    home_city = models.CharField(max_length=150, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(max_length=500, blank=True, null=True)

    is_active = models.BooleanField(default=False)  # initially False, activate after OTP
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = Manager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "phone"]

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["country", "city"])]
        verbose_name = "User"
        verbose_name_plural = "Users"

    @property
    def image_tag(self):
        # getattr() returns the value of an attribute.
        # If the attribute does not exist, it returns the default value (if provided).
        img = getattr(self, 'image', None)
        # hasattr() checks if an object has a specific attribute.
        # It returns True if the attribute exists, otherwise False.
        if img and hasattr(img, 'url'):
            return mark_safe(
                f'<img src="{img.url}" style="max-width:50px; max-height:50px;" />'
            )
        return mark_safe('<span>No Image</span>')

    def __str__(self):
        return self.username

# OTP Model
class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_hash = models.CharField(max_length=64)  # SHA256 hash
    is_used = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return not self.is_used and timezone.now() <= self.created_at + timedelta(minutes=5)

    @staticmethod
    def hash_otp(otp):
        return hashlib.sha256(otp.encode()).hexdigest()
    
    def __str__(self):
        return f"OTP for {self.user.username}"
