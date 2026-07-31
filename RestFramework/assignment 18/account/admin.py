from django.contrib import admin
from django.utils.html import format_html
from account.models import User, OTP


# =========================
# USER ADMIN 
# =========================
@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "username",
        "email",
        "phone",
        "is_verified",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_seen",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "is_verified",
        "is_active",
        "is_staff",
        "is_superuser",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "username",
        "email",
        "phone",
        "country",
        "city",
        "home_city",
        "zip_code",
        "address",
    )

    readonly_fields = (
        "password",
        "last_seen",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Basic Info", {
            "fields": (
                "username",
                "email",
                "phone",
                "password",
            )
        }),
        ("Profile Info", {
            "fields": (
                "image",
                "country",
                "city",
                "home_city",
                "zip_code",
                "address",
            )
        }),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "is_verified",
            )
        }),
        ("Activity", {
            "fields": (
                "is_online",
                "last_seen",
                "last_active",
            )
        }),
        ("Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    ordering = ("-created_at",)


# =========================
# OTP ADMIN 
# =========================
@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "otp_status", "attempt_count", "blocked_until", "is_used", "created_at",)

    list_filter = (
        "blocked_until",
        "is_used",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "user__phone",
    )

    readonly_fields = (
        "user",
        "otp_type",
        "otp_hash",
        "otp_salt",
        "attempt_count",
        "blocked_until",
        "is_used",
        "created_at",
    )

    fieldsets = (
        ("User Info", {
            "fields": (
                "user",
            )
        }),
        ("OTP Security Data", {
            "fields": (
                "otp_hash",
                "otp_salt",
            )
        }),
        ("Status Info", {
            "fields": (
                "attempt_count",
                "blocked_until",
                "is_used",
            )
        }),
        ("Timestamp", {
            "fields": (
                "created_at",
            )
        }),
    )

    ordering = ("-created_at",)

    # =========================
    # OTP STATUS DISPLAY
    # =========================
    def otp_status(self, obj):

        if obj.is_blocked:
            return format_html("<span style='color:red;font-weight:bold;'>BLOCKED</span>")

        if obj.is_expired:
            return format_html("<span style='color:orange;font-weight:bold;'>EXPIRED</span>")

        return format_html("<span style='color:blue;font-weight:bold;'>ACTIVE</span>")

    otp_status.short_description = "Status"