from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']