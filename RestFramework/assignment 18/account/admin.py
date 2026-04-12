from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import User, OTP


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "phone",
        "image_tag",
        "country",
        "city",
        "home_city",
        "zip_code",
        "address",
        "is_active",
        "is_staff",
        "is_superuser",
        "is_verified",
        "is_online",
        "last_seen",
        "last_active",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "is_verified",
        "is_online",
        "country",
        "city",
        "created_at",
    )

    search_fields = (
        "username",
        "email",
        "phone",
        "country",
        "city",
        "home_city",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "image_tag",
        "last_seen",
        "last_active",
        "created_at",
        "updated_at",
        "last_login",
    )

    fieldsets = (
        ("Basic Info", {
            "fields": ("username", "email", "phone", "password")
        }),
        ("Profile Info", {
            "fields": ("image", "country", "city", "home_city", "zip_code", "address")
        }),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser", "is_verified", "groups", "user_permissions")
        }),
        ("Status", {
            "fields": ("is_online", "last_seen", "last_active")
        }),
        ("Timestamps", {
            "fields": ("last_login", "created_at", "updated_at")
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "phone", "password1", "password2"),
        }),
    )

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No Image"
    image_tag.short_description = "Image"


    actions = ["mark_online", "mark_offline"]

    def mark_online(self, request, queryset):
        queryset.update(is_online=True, last_seen=timezone.now())

    def mark_offline(self, request, queryset):
        queryset.update(is_online=False, last_seen=timezone.now())
        



@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "otp_hash",
        "otp_salt",
        "ip_address",
        "is_used",
        "attempt_count",
        "blocked_until",
        "created_at",
        "otp_status",
    )

    list_filter = (
        "is_used",
        "created_at",
        "user__is_verified",
    )

    search_fields = (
        "user__username",
        "user__email",
        "user__phone",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "otp_hash",
        "otp_salt",
        "created_at",
    )

    fieldsets = (
        ("OTP Info", {
            "fields": ("user", "otp_hash", "otp_salt")
        }),
        ("Status Info", {
            "fields": ("is_used", "attempt_count", "blocked_until")
        }),
        ("Time Info", {
            "fields": ("created_at",)
        }),
    )

    def otp_status(self, obj):
        if obj.is_used:
            return format_html('<b style="color:gray">USED</b>')
        if obj.is_blocked():
            return format_html('<b style="color:red">BLOCKED</b>')
        if obj.is_expired():
            return format_html('<b style="color:orange">EXPIRED</b>')
        return format_html('<b style="color:green">ACTIVE</b>')

    otp_status.short_description = "Status"

    actions = ["invalidate_otp", "reset_attempts"]

    def invalidate_otp(self, request, queryset):
        updated = queryset.update(is_used=True)
        self.message_user(request, f"{updated} OTPs invalidated.")

    def reset_attempts(self, request, queryset):
        updated = queryset.update(attempt_count=0, blocked_until=None)
        self.message_user(request, f"{updated} OTPs reset.")