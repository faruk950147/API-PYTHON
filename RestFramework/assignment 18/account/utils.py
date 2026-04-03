import threading
from django.core.mail import send_mail
from django.conf import settings

def send_otp_email(user, otp):
    subject = "Your OTP Code"
    message = f"Hello {user.username},\n\nYour OTP is: {otp}\nThis OTP will expire in 5 minutes."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    # Threaded email sending
    threading.Thread(target=send_mail, args=(subject, message, from_email, recipient_list)).start()