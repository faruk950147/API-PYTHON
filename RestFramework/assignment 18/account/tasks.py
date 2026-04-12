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
    # SETTINGS
    # =========================
    expiry = settings.OTP_EXPIRY_MINUTES

    from_email = getattr(
        settings,
        "DEFAULT_FROM_EMAIL",
        settings.EMAIL_HOST_USER
    )

    # =========================
    # EMAIL CONTENT
    # =========================
    subject = "Your OTP Verification Code"

    message = f"""
        Hello {user.username},

        Your OTP is: {otp_code}

        This OTP will expire in {expiry} minutes.

        If you did not request this, please ignore this email.
        """

    # =========================
    # SEND EMAIL
    # =========================
    send_mail(
        subject,
        message,
        from_email,
        [user.email],
        fail_silently=False
    )

    return "OTP sent successfully"