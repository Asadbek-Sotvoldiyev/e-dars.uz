from django import forms
from admin_panel.models import User, Lesson
from django.core.exceptions import ValidationError


class TeacherProfileForm(forms.ModelForm):
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


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = '__all__'
