from django.db import models, transaction
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.utils.html import mark_safe
from django.utils import timezone
from datetime import timedelta
import hashlib, hmac, secrets
from django.conf import settings

# =========================
# Validators
# =========================
phone_validator = RegexValidator(r"^\+?\d{10,15}$", "Enter a valid phone number")

# =========================
# User Manager
# =========================
class Manager(BaseUserManager):

    def normalize_phone(self, phone):
        if phone.startswith("+880"):
            return phone
        if phone.startswith("01"):
            return "+880" + phone[1:]
        return phone

    def create_user(self, username, email, phone, password=None, **extra_fields):
        if not username:
            raise ValueError("Username is required")
        if not email:
            raise ValueError("Email is required")
        if not phone:
            raise ValueError("Phone is required")

        email = self.normalize_email(email)
        phone = self.normalize_phone(phone)

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
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(username, email, phone, password, **extra_fields)

# =========================
# User Model
# =========================
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True, validators=[UnicodeUsernameValidator()])
    email = models.EmailField(unique=True, db_index=True)
    phone = models.CharField(max_length=15, unique=True, validators=[phone_validator], db_index=True)

    image = models.ImageField(upload_to="users/", blank=True, null=True)

    country = models.CharField(max_length=150, blank=True, null=True, db_index=True)
    city = models.CharField(max_length=150, blank=True, null=True, db_index=True)
    home_city = models.CharField(max_length=150, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(max_length=500, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = Manager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "phone"]
    EMAIL_FIELD = "email"

    class Meta:
        db_table = "user"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["country", "city"])]

    def __str__(self):
        return self.username

    @property
    def image_tag(self):
        if self.image and hasattr(self.image, "url"):
            return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
        return mark_safe("<span>No Image</span>")

# =========================
# OTP Model
# =========================
class OTP(models.Model):
    OTP_EXPIRY_MINUTES = 5
    MAX_ATTEMPTS = 5

    OTP_TYPE_CHOICES = (
        ("register", "Register"),
        ("login", "Login"),
        ("reset", "Password Reset"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otps")
    otp_type = models.CharField(max_length=20, choices=OTP_TYPE_CHOICES)
    otp_hash = models.CharField(max_length=64)
    otp_salt = models.CharField(max_length=16)  # added salt
    is_used = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "otp"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "created_at"]),
            models.Index(fields=["user", "is_used"]),
            models.Index(fields=["otp_type", "is_used"]),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.otp_type}"

    # =========================
    # OTP Logic
    # =========================
    def is_valid(self):
        return (
            not self.is_used
            and self.attempts < self.MAX_ATTEMPTS
            and timezone.now() <= self.created_at + timedelta(minutes=self.OTP_EXPIRY_MINUTES)
        )

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=self.OTP_EXPIRY_MINUTES)

    def verify_otp(self, otp):
        if not self.is_valid():
            return False

        if hmac.compare_digest(self.hash_otp(otp, self.otp_salt), self.otp_hash):
            with transaction.atomic():
                self.is_used = True
                if self.otp_type == "register":
                    self.user.is_verified = True
                    self.user.save(update_fields=["is_verified"])
                self.save(update_fields=["is_used"])
            return True

        self.attempts += 1
        self.save(update_fields=["attempts"])
        return False

    @staticmethod
    def hash_otp(otp, salt):
        if not otp.isdigit() or len(otp) != 6:
            raise ValueError("OTP must be 6 digit number")
        return hashlib.sha256((otp + salt + settings.OTP_SECRET_KEY).encode()).hexdigest()

    @classmethod
    def create_otp(cls, user, otp, otp_type):
        with transaction.atomic():
            last_otp = cls.objects.filter(user=user, otp_type=otp_type).select_for_update().order_by("-created_at").first()
            if last_otp and timezone.now() < last_otp.created_at + timedelta(seconds=60):
                raise ValueError("Wait 60 seconds before requesting another OTP")

            cls.objects.filter(user=user, otp_type=otp_type, is_used=False).update(is_used=True)

            salt = secrets.token_hex(8)
            return cls.objects.create(user=user, otp_type=otp_type, otp_salt=salt, otp_hash=cls.hash_otp(otp, salt))