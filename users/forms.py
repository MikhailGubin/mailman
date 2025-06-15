from django import forms
from django.contrib.auth.forms import UserCreationForm

from mixin_form import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Форма для регистрации Пользователя"""

    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class UserForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = User
        fields = (
            "email",
            "phone_number",
            "avatar",
            "country",
        )
