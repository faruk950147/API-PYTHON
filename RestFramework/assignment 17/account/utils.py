import random
from django.core.mail import send_mail
from account.models import OTP

def generate_otp():
    return str(random.randint(100000, 999999))  # 6-digit OTP

def send_otp_email(user):
    otp = generate_otp()
    otp_hash = OTP.hash_otp(otp)
    OTP.objects.create(user=user, otp_hash=otp_hash)

    subject = "Your Secure OTP Code"
    message = f"""
        Your OTP Code is: {otp}

        This code is valid for 5 minutes and can only be used once.
    """
    send_mail(subject, message, None, [user.email], fail_silently=False)