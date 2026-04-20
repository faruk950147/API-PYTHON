from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from account.models import OTP


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={'max_retries': 3}
)
def send_otp_email(self, otp_id, otp_code):

    try:
        otp_obj = OTP.objects.select_related("user").get(id=otp_id)
    except OTP.DoesNotExist:
        return "OTP not found"

    user = otp_obj.user

    if otp_obj.is_expired:
        return "OTP expired"

    subject = "Your OTP Verification Code"

    message = f"""
    Hello {user.username},

    Your OTP Code: {otp_code}

    This OTP will expire in {settings.OTP_EXPIRY_MINUTES} minutes.

    If you did not request this, ignore this email.

    Thanks,
    System Team
    """

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False
    )

    return "OTP sent successfully"

@shared_task
def cleanup_otps():
    deleted_count, _ = OTP.cleanup_otps()
    return f"{deleted_count} OTPs deleted"

