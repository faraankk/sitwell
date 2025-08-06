from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .forms import SignUpForm, OTPForm, NewPasswordForm
from .models import CustomUser
from .utils import generate_otp, send_otp_email
import random
import string

# ---------- 1. Sign-up ----------

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.is_active = False  # User is inactive until OTP is verified
            user.otp = generate_otp()
            user.otp_created_at = timezone.now()
            user.save()
            send_otp_email(user.email, user.otp)
            request.session['otp_user_id'] = user.id
            messages.success(request, 'OTP sent to your email.')
            return redirect('verify_otp_signup')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# ---------- 2. OTP after sign-up ----------
def verify_otp_signup_view(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user_id = request.session.get('otp_user_id')
        if user_id and otp:
            user = CustomUser.objects.get(pk=user_id)
            if otp == user.otp and timezone.now() < user.otp_created_at + timezone.timedelta(minutes=2):
                user.is_active = True
                user.otp = None
                user.otp_created_at = None
                user.save()
                request.session.pop('otp_user_id', None)
                messages.success(request, 'Account verified. Please log in.')
                return redirect('login')
            else:
                messages.error(request, 'Invalid or expired OTP.')
    else:
        user_id = request.GET.get('resend')
        if user_id:
            user = CustomUser.objects.get(pk=user_id)
            user.otp = generate_otp()
            user.otp_created_at = timezone.now()
            user.save()
            send_otp_email(user.email, user.otp)
            messages.info(request, 'A new OTP has been sent.')
    
    return render(request, 'verify_otp.html')

# ---------- 3. Log-in ----------
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user and user.is_active:
                login(request, user)
                return redirect('home')         # dummy page
            else:
                messages.error(request, 'Invalid credentials.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# ---------- 4. Forgot password ----------
def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            request.session['reset_user_id'] = user.id
            messages.success(request, 'OTP sent to your email.')
            return redirect('verify_otp_forgot')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Email not found.')
    return render(request, 'forgot_password.html')

# ---------- 5. OTP for forgot ----------
def verify_otp_forgot_view(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if otp:                                 # accept any OTP for demo
            return redirect('new_password')
    return render(request, 'verify_otp.html')

# ---------- 6. New password ----------
def new_password_view(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('login')
    user = CustomUser.objects.get(pk=user_id)

    if request.method == 'POST':
        form = NewPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['password'])
            user.save()
            request.session.pop('reset_user_id', None)
            messages.success(request, 'Password changed. Please log in.')
            return redirect('login')
    else:
        form = NewPasswordForm()
    return render(request, 'new_password.html', {'form': form})

# ---------- 7. Dummy home ----------
def home_view(request):
    return render(request, 'home.html')

'''8.generate otp'''
def generate_otp():
    otp = ''.join(random.choices(string.digits, k=6))
    print(f"Generated OTP: {otp}")  # Debugging output
    return otp
