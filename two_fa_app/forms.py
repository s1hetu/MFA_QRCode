from django.contrib.auth.forms import UserCreationForm
from django.forms import Form, ModelForm

from .models import User


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
