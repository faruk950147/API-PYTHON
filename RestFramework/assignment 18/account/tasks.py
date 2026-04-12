from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={'max_retries': 3}
)
def send_otp_email(self, otp_id, otp_code):

    from account.models import OTP

    # =========================
    # GET OTP OBJECT
    # =========================
    try:
        otp_obj = OTP.objects.select_related("user").get(id=otp_id)
    except OTP.DoesNotExist:
        return "OTP not found"

    user = otp_obj.user

    # =========================
    # EMAIL CONFIG
    # =========================
    expiry = settings.OTP_EXPIRY_MINUTES

    from_email = getattr(
        settings,
        "DEFAULT_FROM_EMAIL",
        settings.EMAIL_HOST_USER
    )

    # =========================
    # CLEAN MESSAGE (IMPORTANT FIX)
    # =========================
    message = (
        f"Hello {user.username},\n\n"
        f"Your OTP is: {otp_code}\n\n"
        f"This OTP will expire in {expiry} minutes.\n\n"
        f"If you did not request this, please ignore this email."
    )

    # =========================
    # SEND EMAIL
    # =========================
    send_mail(
        subject="Your OTP Verification Code",
        message=message,
        from_email=from_email,
        recipient_list=[user.email],
        fail_silently=False
    )

    return "OTP sent successfully"