from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()
"""
SignUp form
"""
class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(
        min_length=8,
        max_length=15,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Password"
    )
    password2 = forms.CharField(
        min_length=8,
        max_length=15,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ['username', 'phone', 'email']

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


"""
SignIn form
"""
class SignInForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Username or Email'})
    )
    password = forms.CharField(
        min_length=8,
        max_length=15,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


"""
Reset password form
"""
class ResetPasswordForm(forms.Form):
    email = forms.EmailField(
        max_length=150,
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


"""
Reset password confirm form
"""
class ResetPasswordConfirmForm(forms.Form):
    password = forms.CharField(
        min_length=8,
        max_length=15,
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password'})
    )
    password2 = forms.CharField(
        min_length=8,
        max_length=15,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    #  password match validation
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password and password2 and password != password2:
            self.add_error('password2', "Passwords do not match.")
        return cleaned_data


"""
Change password form
"""
class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        min_length=8,
        max_length=15,
        widget=forms.PasswordInput(attrs={'placeholder': 'Current Password'})
    )
    password = forms.CharField(
        min_length=8,
        max_length=15,
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password'})
    )
    password2 = forms.CharField(
        min_length=8,
        max_length=15,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    #  password match validation
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password and password2 and password != password2:
            self.add_error('password2', "Passwords do not match.")
        return cleaned_data
