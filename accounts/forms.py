from django.forms import  ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MyUser


class CreateUserForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = [ 'username', 'first_name', 'last_name', 'email', 'password1', 'password2']

