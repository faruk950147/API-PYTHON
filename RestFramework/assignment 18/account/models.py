from django.db import models, transaction
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.utils import timezone
from django.conf import settings
from django.db.models import Q, F

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
# USER MODEL
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
        verbose_name_plural = "01 -> User"
        db_table = "user"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["phone"]),
            models.Index(fields=["username"]),
        ]

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)

    # =========================
    # STATUS METHODS
    # =========================
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
# OTP MODEL
# =========================
class OTP(models.Model):

    OTP_LENGTH = getattr(settings, "OTP_LENGTH", 6)
    OTP_EXPIRY_MINUTES = getattr(settings, "OTP_EXPIRY_MINUTES", 5)
    RESEND_INTERVAL = getattr(settings, "OTP_RESEND_INTERVAL", 60)
    MAX_TRIES = getattr(settings, "OTP_MAX_TRIES", 5)
    BLOCK_TIME = getattr(settings, "OTP_BLOCK_TIME", 300)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="otps"
    )

    otp_hash = models.CharField(max_length=64)
    otp_salt = models.CharField(max_length=32)

    attempt_count = models.PositiveIntegerField(default=0)
    blocked_until = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "02 -> OTP"
        db_table = "otp"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "created_at"]),
        ]

    # =========================
    # PROPERTIES
    # =========================
    @property
    def is_expired(self):
        return timezone.now() > (
            self.created_at + timedelta(minutes=self.OTP_EXPIRY_MINUTES)
        )

    @property
    def is_blocked(self):
        return (
            self.blocked_until is not None
            and timezone.now() < self.blocked_until
        )

    # =========================
    # HASH OTP
    # =========================
    @staticmethod
    def hash_otp(otp, salt):
        return hmac.new(
            settings.OTP_SECRET_KEY.encode(),
            f"{otp}{salt}".encode(),
            hashlib.sha256
        ).hexdigest()

    # =========================
    # GENERATE OTP
    # =========================
    @classmethod
    def generate_otp(cls):
        return ''.join(
            secrets.choice("0123456789")
            for _ in range(cls.OTP_LENGTH)
        )

    # =========================
    # CREATE OTP
    # =========================
    @classmethod
    def create_otp(cls, user):

        with transaction.atomic():

            now = timezone.now()

            last_otp = (
                cls.objects
                .filter(user=user)
                .order_by("-created_at")
                .only("created_at")
                .first()
            )

            if last_otp:
                elapsed = (now - last_otp.created_at).total_seconds()

                if elapsed < cls.RESEND_INTERVAL:
                    return {
                        "success": False,
                        "message": f"Wait {int(cls.RESEND_INTERVAL - elapsed)} sec"
                    }

            cls.objects.filter(user=user).delete()

            otp = cls.generate_otp()
            salt = secrets.token_hex(16)

            obj = cls.objects.create(
                user=user,
                otp_hash=cls.hash_otp(otp, salt),
                otp_salt=salt
            )

            from account.tasks import send_otp_email
            send_otp_email.delay(obj.id, otp)

            return {"success": True, "otp_id": obj.id}

    # =========================
    # VERIFY OTP
    # =========================
    @classmethod
    def verify_otp(cls, user, otp_code):

        with transaction.atomic():

            now = timezone.now()

            otp_obj = (
                cls.objects
                .select_for_update()
                .filter(user=user)
                .order_by("-created_at")
                .first()
            )

            if not otp_obj:
                return {"success": False, "message": "Invalid OTP"}

            if otp_obj.is_blocked:
                remain = int((otp_obj.blocked_until - now).total_seconds())
                return {"success": False, "message": f"Blocked {remain}s"}

            if otp_obj.is_expired:
                otp_obj.delete()
                return {"success": False, "message": "Expired OTP"}

            hashed = cls.hash_otp(otp_code, otp_obj.otp_salt)

            if hmac.compare_digest(hashed, otp_obj.otp_hash):

                from django.contrib.auth import get_user_model
                User = get_user_model()

                User.objects.filter(id=user.id).update(is_verified=True)
                otp_obj.delete()

                return {"success": True, "message": "Verified"}

            # increase attempt count atomically
            cls.objects.filter(id=otp_obj.id).update(
                attempt_count=F("attempt_count") + 1
            )

            otp_obj.refresh_from_db()

            if otp_obj.attempt_count >= cls.MAX_TRIES:
                cls.objects.filter(id=otp_obj.id).update(
                    blocked_until=now + timedelta(seconds=cls.BLOCK_TIME)
                )

            return {"success": False, "message": "Invalid OTP"}

    # =========================
    # CLEANUP TASK
    # =========================
    @classmethod
    def cleanup_otps(cls):
        now = timezone.now()

        deleted, _ = cls.objects.filter(
            Q(created_at__lt=now - timedelta(minutes=cls.OTP_EXPIRY_MINUTES)) |
            (Q(blocked_until__isnull=False) & Q(blocked_until__lt=now))
        ).delete()

        return deleted