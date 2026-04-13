from django.db import models, transaction
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.utils import timezone
from django.conf import settings

import hashlib
import hmac
import secrets
import re
from datetime import timedelta

# =========================
# PHONE VALIDATOR
# =========================
phone_validator = RegexValidator(
    r"^\+?\d{10,15}$",
    "Enter a valid phone number"
)


# =========================
# USER MANAGER
# =========================
class UserManager(BaseUserManager):
    def normalize_phone(self, phone):
        phone = re.sub(r"\s+", "", phone)

        if phone.startswith("+880"):
            return phone
        if phone.startswith("880"):
            return "+" + phone
        if phone.startswith("01"):
            return "+880" + phone[1:]

        return phone

    def create_user(self, username, email, phone, password=None, **extra_fields):
        if not username:
            raise ValueError("Username required")
        if not email:
            raise ValueError("Email required")
        if not phone:
            raise ValueError("Phone required")

        email = self.normalize_email(email)
        phone = self.normalize_phone(phone)

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

        return self.create_user(username, email, phone, password, **extra_fields)


# =========================
# USER MODEL (PRODUCTION READY)
# =========================
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True, validators=[phone_validator])

    image = models.ImageField(upload_to="users/", blank=True, null=True)

    country = models.CharField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    home_city = models.CharField(max_length=150, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True, blank=True)
    last_active = models.DateTimeField(default=timezone.now)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "phone"]

    class Meta:
        verbose_name_plural = "01. Users"
        db_table = "user"
        ordering = ["-created_at"]
        # indexes for faster lookups on common queries like 
        # email, phone, active status, verification status, and online status
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["phone"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["is_verified"]),
            models.Index(fields=["is_online"]),
        ]

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)

    def mark_online(self):
        self.is_online = True
        self.last_seen = timezone.now()
        self.save(update_fields=["is_online", "last_seen"])

    def mark_offline(self):
        self.is_online = False
        self.last_seen = timezone.now()
        self.save(update_fields=["is_online", "last_seen"])

    def mark_active(self):
        self.last_active = timezone.now()
        self.save(update_fields=["last_active"])


# =========================
# OTP MODEL (PRODUCTION READY)
# =========================
class OTP(models.Model):
    OTP_LENGTH = getattr(settings, "OTP_LENGTH", 6)
    OTP_EXPIRY_MINUTES = getattr(settings, "OTP_EXPIRY_MINUTES", 5)
    RESEND_INTERVAL = getattr(settings, "OTP_RESEND_INTERVAL", 60)
    MAX_TRIES = getattr(settings, "OTP_MAX_TRIES", 5)
    BLOCK_TIME = getattr(settings, "OTP_BLOCK_TIME", 300)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otps")

    otp_hash = models.CharField(max_length=64)
    otp_salt = models.CharField(max_length=32)

    ip_address = models.GenericIPAddressField(null=True, blank=True)

    is_used = models.BooleanField(default=False)
    attempt_count = models.PositiveIntegerField(default=0)

    blocked_until = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "02. OTPs"
        db_table = "otp"
        ordering = ["-created_at"]

        # indexes for faster lookups on common queries like 
        # user, used status, creation time, and IP address
        indexes = [
            models.Index(fields=["user", "is_used"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["ip_address"]),
        ]

    # =========================
    # HASH OTP
    # =========================
    @staticmethod
    def hash_otp(otp, salt):
        secret = settings.OTP_SECRET_KEY
        return hmac.new(
            secret.encode(),
            f"{otp}{salt}".encode(),
            hashlib.sha256
        ).hexdigest()

    # =========================
    # GENERATE OTP
    # =========================
    @classmethod
    def generate_otp(cls):
        return ''.join(secrets.choice("0123456789") for _ in range(cls.OTP_LENGTH))

    # =========================
    # EXPIRE CHECK
    # =========================
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=self.OTP_EXPIRY_MINUTES)

    # =========================
    # BLOCK CHECK
    # =========================
    def is_blocked(self):
        return self.blocked_until is not None and timezone.now() < self.blocked_until

    # =========================
    # CREATE OTP (PRODUCTION SAFE)
    # =========================
    @classmethod
    def create_otp(cls, user, ip=None):
        with transaction.atomic():
            last = cls.objects.filter(user=user, is_used=False).order_by("-created_at").first()

            if last and last.created_at + timedelta(seconds=cls.RESEND_INTERVAL) > timezone.now():
                wait = (last.created_at + timedelta(seconds=cls.RESEND_INTERVAL)) - timezone.now()
                return {
                    "success": False,
                    "message": f"Wait {int(wait.total_seconds())} seconds"
                }

            cls.objects.filter(user=user, is_used=False).update(is_used=True)

            otp = cls.generate_otp()
            salt = secrets.token_hex(16)

            obj = cls.objects.create(
                user=user,
                otp_hash=cls.hash_otp(otp, salt),
                otp_salt=salt,
                ip_address=ip
            )

            # IMPORTANT FIX
            from account.tasks import send_otp_email
            send_otp_email.delay(obj.id, otp)

            return {
                "success": True,
                "otp_id": obj.id
            }

    # =========================
    # VERIFY OTP (PRODUCTION SAFE)
    # =========================
    @classmethod
    def verify_otp(cls, otp_id, otp_code):
        if not otp_code or not otp_code.isdigit():
            return {"success": False, "message": "Invalid OTP"}

        with transaction.atomic():
            try:
                otp_obj = cls.objects.select_for_update().get(id=otp_id)
            except cls.DoesNotExist:
                return {"success": False, "message": "OTP not found"}

            if otp_obj.is_used:
                return {"success": False, "message": "Already used"}

            if otp_obj.is_blocked():
                return {"success": False, "message": "Blocked"}

            if otp_obj.is_expired():
                return {"success": False, "message": "Expired"}

            hashed = cls.hash_otp(otp_code, otp_obj.otp_salt)

            if hmac.compare_digest(hashed, otp_obj.otp_hash):
                otp_obj.is_used = True
                otp_obj.save(update_fields=["is_used"])

                otp_obj.user.is_verified = True
                otp_obj.user.save(update_fields=["is_verified"])

                return {"success": True, "message": "Verified"}

            # wrong OTP
            otp_obj.attempt_count += 1

            if otp_obj.attempt_count >= cls.MAX_TRIES:
                otp_obj.blocked_until = timezone.now() + timedelta(seconds=cls.BLOCK_TIME)
                otp_obj.attempt_count = 0  # reset after block

            otp_obj.save(update_fields=["attempt_count", "blocked_until"])

            return {"success": False, "message": "Wrong OTP"}

    # =========================
    # CLEANUP TASK
    # =========================
    @classmethod
    def expired_otp_clear(cls):
        expiry_time = timezone.now() - timedelta(minutes=cls.OTP_EXPIRY_MINUTES)
        cls.objects.filter(created_at__lt=expiry_time).delete()