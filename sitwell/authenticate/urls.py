from django.urls import path
from . import views

urlpatterns = [
    path('signup/',          views.signup_view,          name='signup'),
    path('verify-otp-sign/', views.verify_otp_signup_view, name='verify_otp_signup'),
    path('login/',           views.login_view,           name='login'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('verify-otp/',      views.verify_otp_forgot_view, name='verify_otp_forgot'),
    path('new-password/',    views.new_password_view,    name='new_password'),
    path('',                 views.home_view,            name='home'),
]