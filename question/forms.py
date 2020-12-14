from django import forms
from django.forms.widgets import PasswordInput


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=PasswordInput)
