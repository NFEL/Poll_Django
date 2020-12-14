from django import forms
from django.forms.widgets import PasswordInput


from .models import Question,Choice

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=PasswordInput)

class QuestionForm(forms.ModelForm):
    
    class Meta:
        model = Question
        fields = ("q_name",)

class ChoiceForm(forms.ModelForm):
    
    class Meta:
        model = Choice
        fields = ("c_name","question",)
