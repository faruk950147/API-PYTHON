from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.contrib.auth import get_user_model


from account.models import OTP
User = get_user_model()


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries': 3})
def send_otp_email(self, otp_id, otp_code):
    verify_url = f"{settings.BASE_URL}/api/account/verify-otp/"

    try:
        otp_obj = OTP.objects.select_related("user").get(id=otp_id)
    except OTP.DoesNotExist:
        return "OTP not found"

    if otp_obj.is_expired:
        otp_obj.delete()
        return "OTP expired"

    user = otp_obj.user

    message = f"""
    Hello {user.username},

    Your OTP is: {otp_code}

    This OTP will expire in {settings.OTP_EXPIRY_MINUTES} minutes.

    Send POST request to:
    {verify_url}

    Body:
    {{  
        "email": "{user.email}"
        "otp": "{otp_code}"
    }}

    If you did not request this, ignore this email.
    """

    send_mail(
        subject="Your OTP Verification Code",
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False
    )

    return "OTP sent successfully"

# Auto delete otp
@shared_task
def cleanup_otps():
    return OTP.cleanup_otps()