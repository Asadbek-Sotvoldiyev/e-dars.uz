from random import random

from django import forms
from .models import User
from django.core.exceptions import ValidationError


class AdminProfileForm(forms.ModelForm):
    username = forms.CharField(label="Username", disabled=True)
    first_name = forms.CharField(label='Ism', widget=forms.TextInput())
    last_name = forms.CharField(label='Familiya', widget=forms.TextInput())
    email = forms.EmailField(label='Email', widget=forms.EmailInput())
    phone = forms.CharField(label='Telefon raqam', widget=forms.TextInput())
    birthday = forms.DateField(label='Tug\'ilgan sana', widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'phone', 'birthday', 'gender', 'image')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists() and email != self.instance.email:
            raise ValidationError("Email already exists")
        return email


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserForm(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'phone', 'gender')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
        }
