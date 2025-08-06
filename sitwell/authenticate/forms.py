from django import forms
from .models import CustomUser

class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone_number')

    def clean(self):
        cleaned = super().clean()
        pw1 = cleaned.get('password1')
        pw2 = cleaned.get('password2')
        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6, label='Enter OTP')


class NewPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('confirm_password'):
            raise forms.ValidationError('Passwords do not match.')
        return cleaned
    
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

# class CustomAuthenticationForm(AuthenticationForm):
#     username = EmailField(label="Email")

#     def clean_username(self):
#         email = self.cleaned_data.get('username')
#         try:
#             user = get_user_model().objects.get(email=email)
#         except get_user_model().DoesNotExist:
#             raise ValidationError("Invalid email address.")
#         return email
