import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    otp_auth_url = models.CharField(max_length=255, null=True)
    otp_base32 = models.CharField(max_length=255, null=True)
    qrcode = models.ImageField(null=True)
    mfa_activated = models.BooleanField(default=False)
    mfa_otp_verified = models.BooleanField(default=False)
    mfa_expiry_time = models.DateTimeField(default=datetime.datetime.now)