from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import User, OTP

# =========================
# User Admin (All fields)
# =========================
class UserAdmin(admin.ModelAdmin):
    model = User
    # List display configuration
    list_display = (
        "id", "username", "email", "phone", "image_tag",
        "country", "city", "home_city", "zip_code", "address",
        "is_active", "is_staff", "is_verified", "is_superuser",
        "is_online", "last_seen", "last_active",
        "created_at", "updated_at"
    )
    # List filter configuration
    list_filter = (
        "is_active", "is_staff", "is_verified", "is_superuser",
        "is_online", "country", "city", "created_at"
    )
    # Search fields configuration
    search_fields = ("username", "email", "phone", "country", "city", "home_city")
    ordering = ("-created_at",)
    readonly_fields = ("last_seen", "last_active", "image_tag", "created_at", "updated_at", "last_login")
    actions = ["mark_selected_online", "mark_selected_offline"]
    # Fieldsets configuration it works like a form with sections
    fieldsets = (
        (None, {"fields": ("username", "email", "phone", "password")}),
        ("Profile Info", {"fields": ("image", "country", "city", "home_city", "zip_code", "address")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "is_verified", "groups", "user_permissions")}),
        ("Status", {"fields": ("is_online", "last_seen", "last_active")}),
        ("Important Dates", {"fields": ("last_login", "created_at", "updated_at")}),
    )
    # Add fieldsets configuration it works like a form with sections
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "phone", "password1", "password2", "is_active", "is_staff", "is_verified"),
        }),
    )
    # Get readonly fields configuration
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("username", "email", "phone")
        return self.readonly_fields
    
    # Mark selected online method
    def mark_selected_online(self, request, queryset):
        queryset.update(is_online=True, last_seen=timezone.now())
    mark_selected_online.short_description = "Mark selected users as Online"

    # Mark selected offline method
    def mark_selected_offline(self, request, queryset):
        queryset.update(is_online=False, last_seen=timezone.now())
    mark_selected_offline.short_description = "Mark selected users as Offline"

    # Image tag method
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No Image"


# =========================
# OTP Admin (All fields)
# =========================
class OTPAdmin(admin.ModelAdmin):
    model = OTP
    list_display = (
        "id", "user", "otp_preview", "otp_hash", "otp_salt",
        "is_used", "used_count", "otp_status", "created_at"
    )
    # List filter configuration
    list_filter = ("is_used", "user__is_verified", "created_at")
    # Search fields configuration   
    search_fields = ("user__username", "user__email", "user__phone")
    # Read only fields configuration
    readonly_fields = ("otp_hash", "otp_salt", "created_at")
    # Actions configuration
    actions = ["invalidate_selected_otps", "resend_selected_otps"]
    # Fieldsets configuration it works like a form with sections
    fieldsets = (
        (None, {"fields": ("user", "otp_hash", "otp_salt", "is_used", "used_count", "created_at")}),
    )
    # OTP preview method
    def otp_preview(self, obj):
        return format_html("<b>****{}</b>", obj.otp_hash[-4:])
    otp_preview.short_description = "OTP Hash Preview"

    # OTP status method
    def otp_status(self, obj):
        color = "red" if obj.is_expired() else "green"
        status = "Expired" if obj.is_expired() else "Valid"
        return format_html('<b style="color:{}">{}</b>', color, status)
    otp_status.short_description = "Status"


    # Invalidate selected OTPs method
    def invalidate_selected_otps(self, request, queryset):
        updated = queryset.update(is_used=True)
        self.message_user(request, f"{updated} OTPs invalidated successfully.")
    invalidate_selected_otps.short_description = "Invalidate selected OTPs"

    # Resend selected OTPs method
    def resend_selected_otps(self, request, queryset):
        for otp_obj in queryset:
            OTP.create_otp(user=otp_obj.user)
        self.message_user(request, "New OTPs generated for selected users.")
    resend_selected_otps.short_description = "Resend OTPs for selected users"


# Register models
admin.site.register(User, UserAdmin)
admin.site.register(OTP, OTPAdmin)