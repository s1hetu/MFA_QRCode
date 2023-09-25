import datetime

import pyotp
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import qrcode
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView

from two_fa_setup.settings import BASE_DIR
from .forms import RegistrationForm, LoginForm


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'


class Login(View):
    template_name = 'auth/login.html'
    form = LoginForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'login_form': self.form()})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)

        username = form.data.get('username')
        password = form.data.get('password')

        if user := authenticate(username=username, password=password):
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")
            return render(request, self.template_name, {'login_form': form})


class Registration(View):
    form_class = RegistrationForm
    template_name = 'auth/register.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'register_form': self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = form.save()

            otp_base32 = pyotp.random_base32()
            user.otp_base32 = otp_base32
            otp_auth_url = pyotp.totp.TOTP(otp_base32).provisioning_uri(name=username.lower(),
                                                                        issuer_name="hs_gen_web.com")
            user.otp_auth_url = otp_auth_url

            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4, )
            qr.add_data(user.otp_auth_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            image = img.save(f"{BASE_DIR}/media/qr_codes/{user.username}_qrcode.png")
            user.qrcode = f"qr_codes/{user.username}_qrcode.png"
            user.save()
            messages.success(request, "User created successfully.")
            return redirect('login')
        else:
            errors = form.errors
            print("errors", errors)
            messages.error(request, "User creation failed.")
        return render(request, self.template_name, {'register_form': form})


class AuthDetails(TemplateView):
    template_name = 'auth/display_qr_secret.html'


@method_decorator(csrf_exempt, name='post')
class VerifyOTP(LoginRequiredMixin, View):
    template = 'auth/verify_otp.html'

    def post(self, request, *args, **kwargs):
        user = request.user
        entered_otp = request.POST.get('otp')
        if entered_otp:
            if entered_otp.isdigit():
                if len(entered_otp) == 6:
                    otp_base32 = user.otp_base32
                    totp = pyotp.TOTP(otp_base32)
                    if totp.verify(entered_otp):
                        user.mfa_activated = True
                        user.mfa_otp_verified = True
                        user.mfa_expiry_time = datetime.datetime.now() + datetime.timedelta(minutes=10)
                        return_msg = {"msg": "OTP Verified."}
                    else:
                        return_msg = {"msg": "Invalid OTP."}
                else:
                    return_msg = {"msg": "Length of OTP should e 6."}
            else:
                return_msg = {"msg": "OTP should be int only."}
        else:
            return_msg = {"msg": "OTP cant be empty."}

        return JsonResponse(return_msg)


class Logout(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect('/')
