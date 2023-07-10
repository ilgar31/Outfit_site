from django.contrib.auth.models import User
from .models import Profile
from django.forms import ModelForm, CharField, PasswordInput, TextInput, EmailInput, DateInput, FileInput, TextInput


class UserRegistrationForm(ModelForm):
    password = CharField(label='Password', widget=PasswordInput(attrs={"placeholder": "Придумайте пароль", "style": "padding-left: 10px; font-size: 16px;"}))

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': EmailInput(attrs={'placeholder': 'Введите адрес электронной почты', "style": "padding-left: 10px; font-size: 16px;"}),
        }


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = {"img", "user_name", "user_surname", "birthday", "gender", "country"}
        widgets = {
            "img": FileInput(attrs={'class': 'change_img'}),
            "user_name": TextInput(attrs={'class': 'change_name'}),
            "user_surname": TextInput(attrs={'class': 'change_surname'}),
            "birthday": DateInput(attrs={'type': 'date', 'class': 'change_birthday'}),
            "gender": TextInput(attrs={'class': 'change_gender'}),
            "country": TextInput(attrs={'class': 'change_country'}),
        }

