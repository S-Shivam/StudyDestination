from django.contrib.auth.models import User
from django import forms
from .models import Country, University


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['name', 'language', 'currency', 'country_pic']


class UniversityForm(forms.ModelForm):
    class Meta:
        model = University
        fields = ['university_name', 'state', 'rank', 'intro_video']

