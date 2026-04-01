from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.utils.html import mark_safe
from django.utils import timezone
from datetime import timedelta
import hashlib
import hmac

# =========================
# Validators
# =========================
phone_validator = RegexValidator(
    r"^\+?\d{10,15}$",
    "Enter a valid phone number"
)

# =========================
# User Manager
# =========================
class Manager(BaseUserManager):
    def create_user(self, username, email, phone, password=None, **extra_fields):
        if not all([username, email, phone]):
            raise ValueError("Username, Email and Phone are required")

        email = self.normalize_email(email)

        user = self.model(
            username=username,
            email=email,
            phone=phone,
            **extra_fields
        )

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
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(username, email, phone, password, **extra_fields)


# =========================
# Custom User Model
# =========================
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[UnicodeUsernameValidator()]
    )
    email = models.EmailField(unique=True, db_index=True)
    phone = models.CharField(
        max_length=15,
        unique=True,
        validators=[phone_validator],
        db_index=True
    )

    image = models.ImageField(upload_to="users/", blank=True, null=True)

    country = models.CharField(max_length=150, blank=True, null=True, db_index=True)
    city = models.CharField(max_length=150, blank=True, null=True, db_index=True)
    home_city = models.CharField(max_length=150, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(max_length=500, blank=True, null=True)

    is_active = models.BooleanField(default=False)   # if OTP verify True
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = Manager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "phone"]

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["country", "city"]),
        ]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username


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


# =========================
# OTP Model
# =========================
class OTP(models.Model):
    OTP_EXPIRY_MINUTES = 5
    MAX_ATTEMPTS = 5

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otps")
    otp_hash = models.CharField(max_length=64)
    is_used = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "created_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - OTP"

    # =========================
    # OTP Methods
    # =========================
    def is_valid(self):
        return (
            not self.is_used
            and self.attempts < self.MAX_ATTEMPTS
            and timezone.now() <= self.created_at + timedelta(minutes=self.OTP_EXPIRY_MINUTES)
        )

    def verify_otp(self, otp):
        if not self.is_valid():
            return False

        # secure compare
        if hmac.compare_digest(self.hash_otp(otp), self.otp_hash):
            self.is_used = True

            # activate user
            self.user.is_active = True
            self.user.is_verified = True
            self.user.save()

            self.save()
            return True

        self.attempts += 1
        self.save()
        return False

    @staticmethod
    def hash_otp(otp):
        return hashlib.sha256(otp.encode()).hexdigest()

    @classmethod
    def create_otp(cls, user, otp):
        # delete previous unused OTP
        cls.objects.filter(user=user, is_used=False).delete()

        return cls.objects.create(
            user=user,
            otp_hash=cls.hash_otp(otp)
        )

