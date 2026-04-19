from django import forms
from django.contrib.auth import get_user_model, authenticate
from account.models import OTP

User = get_user_model()


# =========================
# SIGNUP
# =========================
class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ["username", "email", "phone", "password", "password2"]

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data["password"] != cleaned_data["password2"]:
            raise forms.ValidationError("Password mismatch")

        return cleaned_data

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            phone=self.cleaned_data["phone"],
            password=self.cleaned_data["password"]
        )

        OTP.create_otp(user=user)

        return user


# =========================
# OTP VERIFY
# =========================
class OTPVerifyForm(forms.Form):
    email = forms.EmailField()
    otp = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()

        try:
            user = User.objects.get(
                email=cleaned_data["email"]
            )
        except User.DoesNotExist:
            raise forms.ValidationError("User not found")

        if user.is_verified:
            raise forms.ValidationError("Already verified")

        result = OTP.verify_otp(
            user,
            cleaned_data["otp"]
        )

        if not result["success"]:
            raise forms.ValidationError(
                result["message"]
            )

        self.user = user

        return cleaned_data


# =========================
# LOGIN
# =========================
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()

        user = authenticate(
            username=cleaned_data["username"],
            password=cleaned_data["password"]
        )

        if not user:
            raise forms.ValidationError(
                "Invalid credentials"
            )

        if not user.is_active:
            raise forms.ValidationError(
                "Inactive user"
            )

        if not user.is_verified:
            raise forms.ValidationError(
                "Not verified"
            )

        self.user = user

        return cleaned_data


# =========================
# CHANGE PASSWORD
# =========================
class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput
    )

    new_password = forms.CharField(
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        if not self.user.check_password(
            cleaned_data["old_password"]
        ):
            raise forms.ValidationError(
                "Wrong old password"
            )

        if (
            cleaned_data["new_password"] !=
            cleaned_data["confirm_password"]
        ):
            raise forms.ValidationError(
                "Mismatch"
            )

        return cleaned_data

    def save(self):
        self.user.set_password(
            self.cleaned_data["new_password"]
        )

        self.user.save(
            update_fields=["password"]
        )

        return self.user


# =========================
# RESET PASSWORD REQUEST
# =========================
class ResetPasswordRequestForm(forms.Form):
    email = forms.EmailField()

    def clean(self):
        cleaned_data = super().clean()

        try:
            user = User.objects.get(
                email=cleaned_data["email"]
            )
        except User.DoesNotExist:
            raise forms.ValidationError(
                "User not found"
            )

        OTP.create_otp(user=user)

        self.user = user

        return cleaned_data


# =========================
# RESET PASSWORD CONFIRM
# =========================
class ResetPasswordConfirmForm(forms.Form):
    email = forms.EmailField()
    otp = forms.CharField()

    new_password = forms.CharField(
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()

        try:
            user = User.objects.get(
                email=cleaned_data["email"]
            )
        except User.DoesNotExist:
            raise forms.ValidationError(
                "User not found"
            )

        if (
            cleaned_data["new_password"] !=
            cleaned_data["confirm_password"]
        ):
            raise forms.ValidationError(
                "Mismatch"
            )

        result = OTP.verify_otp(
            user,
            cleaned_data["otp"]
        )

        if not result["success"]:
            raise forms.ValidationError(
                result["message"]
            )

        self.user = user

        return cleaned_data

    def save(self):
        self.user.set_password(
            self.cleaned_data["new_password"]
        )

        self.user.save(
            update_fields=["password"]
        )

        return self.user


# =========================
# RESEND OTP
# =========================
class ResendOTPForm(forms.Form):
    email = forms.EmailField()

    def clean(self):
        cleaned_data = super().clean()

        try:
            user = User.objects.get(
                email=cleaned_data["email"]
            )
        except User.DoesNotExist:
            raise forms.ValidationError(
                "User not found"
            )

        OTP.create_otp(user=user)

        self.user = user

        return cleaned_data