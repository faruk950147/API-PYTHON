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
    try:
        otp_obj = OTP.objects.select_related("user").get(id=otp_id)
    except OTP.DoesNotExist:
        return "OTP not found"
        
    # use model property
    if otp_obj.is_expired:
        otp_obj.delete()
        return "OTP expired"

    user = otp_obj.user

    message = (
        f"Hello {user.username},\n\n"
        f"Your OTP is: {otp_code}\n\n"
        f"This OTP will expire in {settings.OTP_EXPIRY_MINUTES} minutes.\n\n"
        f"If you did not request this, ignore this email."
    )

    send_mail(
        subject="Your OTP Verification Code",
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False
    )

    return "OTP sent successfully"


@shared_task
def cleanup_otps_task():
    deleted_count = OTP.cleanup_otps()
    return f"Deleted OTPs: {deleted_count}"
