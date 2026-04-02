import random
from django.core.mail import send_mail
from django.conf import settings
from account.models import OTP
from django.core.exceptions import ValidationError

def generate_otp():
    return "%06d" % random.randint(0, 999999)

def send_otp_email(user):
    otp = generate_otp()
    try:
        OTP.create_otp(user=user, otp=otp, otp_type="register")  # handles hash, salt, transaction
    except ValueError as e:
        # OTP 60 সেকেন্ডের rule ভেঙে গেলে exception throw হয়
        raise ValidationError(str(e))

    subject = "Your Secure OTP Code"
    message = f"""
    Your OTP Code is: {otp}

    This code is valid for 5 minutes and can only be used once.
    """
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)