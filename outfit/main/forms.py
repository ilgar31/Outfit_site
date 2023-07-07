from django.contrib.auth.models import User
from django.forms import ModelForm, CharField, PasswordInput, TextInput, EmailInput


class UserRegistrationForm(ModelForm):
    password = CharField(label='Password', widget=PasswordInput(attrs={"placeholder": "Придумайте пароль", "style": "padding-left: 10px; font-size: 16px;"}))

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': EmailInput(attrs={'placeholder': 'Введите адрес электронной почты', "style": "padding-left: 10px; font-size: 16px;"}),
        }
