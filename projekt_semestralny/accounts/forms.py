from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
  username = forms.CharField(label="Nazwa użytkownika")
  password1 = forms.CharField(
    label="Hasło",
    widget=forms.PasswordInput
  )
  password2 = forms.CharField(
    label="Potwierdź hasło",
    widget=forms.PasswordInput
  )

  class Meta:
    model = User
    fields = ("username", "password1", "password2")
