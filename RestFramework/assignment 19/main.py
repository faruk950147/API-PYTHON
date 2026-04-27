from datetime import timedelta, timezone
import hashlib
import hmac
import secrets
import re
from django.conf import settings
from django.db import models, transaction
from django.db import models
from django.contrib.auth.models import User

'''
If your goal is to actually use these modules, here’s a quick summary:

hashlib - Create hashes like SHA256, MD5.
hmac - Generate cryptographic message signatures.
secrets - Generate secure random numbers and tokens (good for passwords, OTPs).
re - Perform regex-based string matching and manipulation.

For example, a simple SHA256 hash:
'''
'''
# ==================================== hashlib ====================================
# Original message
message = "Hello World"

# Hash the message
hash_object = hashlib.sha256(message.encode())
hash_string = hash_object.hexdigest()
print(f"Hash: {hash_string}")

# Verify the message (if message is changed, verification will fail)
check_message = "Hello World"  # Try changing this to see verification fail
check_hash = hashlib.sha256(check_message.encode()).hexdigest()

if check_hash == hash_string:
    print("Message verified! Hash matches.")
else:
    print("Hash mismatch. Message altered!")

# ==================================== hash message authentication code ====================================
original_message = "Hello World"
key = "my_secret_key"  # Must be bytes

# Generate HMAC
# new is a constructor that creates a new HMAC object
h = hmac.new(key.encode(), original_message.encode(), hashlib.sha256) 

# Verify HMAC
check_h = hmac.new(key.encode(), original_message.encode(), hashlib.sha256) 
if check_h.hexdigest() == h.hexdigest():
    print("HMAC verified!")
else:
    print("HMAC mismatch!")
'''
original_message = "Hello World"
key = "my_secret_key"  

secrets_key = hmac.new(key.encode(), original_message.encode(), hashlib.sha256)
print(f"HMAC: {secrets_key.hexdigest()}")

# ==================================== secrets ====================================
# Generate a secure random token
# token = secrets.token_hex(16)
# print(f"Secure token: {token}")

# Generate a secure random integer between 0 and 99
# random_int = secrets.randbelow(100)
# print(f"Random integer a digit: {random_int}") 

# Generate a secure random choice
# choices = ['apple', 'banana', 'cherry']
# random_choice = secrets.choice(choices)
# print(f"Random choice: {random_choice}")



'''

তোমার code ঠিক আছে, শুধু auto delete behavior fix করতে minimal change লাগবে — পুরো corrected version নিচে দিলাম 👇

FINAL FIXED VERSION (only necessary changes applied)
# CREATE OTP
@classmethod
def create_otp(cls, user, ip=None):
    with transaction.atomic():
        now = timezone.now()

        last_otp = (
            cls.objects
            .filter(user=user)
            .order_by("-created_at")
            .first()
        )

        # RESEND LIMIT
        if last_otp:
            elapsed = (now - last_otp.created_at).total_seconds()
            if elapsed < cls.RESEND_INTERVAL:
                return {
                    "success": False,
                    "message": f"Wait {int(cls.RESEND_INTERVAL - elapsed)} sec"
                }

        # DELETE old OTPs instead of marking used
        cls.objects.filter(user=user).delete()

        otp = cls.generate_otp()
        salt = secrets.token_hex(16)

        obj = cls.objects.create(
            user=user,
            otp_hash=cls.hash_otp(otp, salt),
            otp_salt=salt,
            ip_address=ip
        )

        from account.tasks import send_otp_email
        send_otp_email.delay(obj.id, otp)

        return {"success": True, "otp_id": obj.id}
# VERIFY OTP
@classmethod
def verify_otp(cls, user, otp_code):
    with transaction.atomic():
        now = timezone.now()

        otp_obj = (
            cls.objects
            .select_for_update()
            .filter(user=user)
            .order_by("-created_at")
            .first()
        )

        if not otp_obj:
            return {"success": False, "message": "Invalid request"}

        # BLOCK CHECK
        if otp_obj.is_blocked:
            remaining = int((otp_obj.blocked_until - now).total_seconds())
            return {"success": False, "message": f"Blocked. Try after {remaining} sec"}

        # EXPIRE → DELETE
        if otp_obj.is_expired:
            otp_obj.delete()
            return {"success": False, "message": "Expired OTP"}

        # VERIFY HASH
        hashed = cls.hash_otp(otp_code, otp_obj.otp_salt)

        if hmac.compare_digest(hashed, otp_obj.otp_hash):
            otp_obj.user.is_verified = True
            otp_obj.user.save(update_fields=["is_verified"])

            # SUCCESS → DELETE
            otp_obj.delete()

            return {"success": True, "message": "Verified"}

        # WRONG OTP
        otp_obj.attempt_count += 1

        if otp_obj.attempt_count >= cls.MAX_TRIES:
            otp_obj.blocked_until = now + timedelta(seconds=cls.BLOCK_TIME)

        otp_obj.save(update_fields=["attempt_count", "blocked_until"])

        return {"success": False, "message": "Invalid OTP"}
        
        
    # CLEANUP EXPIRED OTPs
    @classmethod
    def cleanup_otps(cls):
        now = timezone.now()
        deleted, _ = cls.objects.filter(Q(created_at__lt=now - timedelta(minutes=cls.OTP_EXPIRY_MINUTES))).delete()
        return deleted


এখন behavior হবে

✔ OTP verify success → delete
✔ OTP expired → delete instantly
✔ new OTP create → old delete
✔ DB clean থাকবে (no junk)

❗ Note (important)

is_used এখন useless হয়ে গেছে
চাইলেই future এ remove করতে পারো (but এখন রাখলেও সমস্যা নাই)


'''
