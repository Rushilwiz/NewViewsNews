from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic']

class ValuesUpdateForm(forms.ModelForm):

    economicScore = forms.IntegerField(label="Economic Score")
    socialScore = forms.IntegerField(label="Social Score")

    class Meta:
        model = Profile
        fields = ['economicScore', 'socialScore']
