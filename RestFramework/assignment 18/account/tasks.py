from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from account.models import OTP


# =========================
# SEND OTP EMAIL
# =========================
@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
    retry_kwargs={"max_retries": 3}
)
def send_otp_email(self, otp_id, otp_code):

    otp_obj = OTP.objects.select_related("user").filter(id=otp_id).first()

    if not otp_obj:
        return {"status": "failed", "reason": "OTP not found"}

    user = otp_obj.user

    subject = "Your OTP Verification Code"

    message = (
        f"Hello {user.username},\n\n"
        f"Your OTP Code: {otp_code}\n\n"
        f"This OTP will expire in {settings.OTP_EXPIRY_MINUTES} minutes.\n\n"
        "If you did not request this, ignore this email.\n\n"
        "Thanks,\nSystem Team"
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False
    )

    return {"status": "success", "message": "OTP sent"}


# =========================
# Resend 
# =========================
@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
    retry_kwargs={"max_retries": 3}
)
def resend_otp_email(self, otp_id):

    otp_obj = OTP.objects.select_related("user").filter(id=otp_id).first()

    if not otp_obj:
        return {"status": "failed", "reason": "OTP not found"}

    if otp_obj.is_used:
        return {"status": "failed", "reason": "OTP already used"}

    user = otp_obj.user

    subject = "Your OTP Code (Resend)"

    message = (
        f"Hello {user.username},\n\n"
        f"Your OTP Code: {otp_obj.otp_hash}\n\n"
        f"Please use it within {settings.OTP_EXPIRY_MINUTES} minutes.\n\n"
        "If you did not request this, ignore this email.\n\n"
        "Thanks,\nSystem Team"
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False
    )

    return {"status": "success", "message": "OTP resent"}

@shared_task
def cleanup_otps():
    deleted_count, _ = OTP.cleanup_otps()
    return f"{deleted_count} OTPs deleted"

