from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm

from mixin_form import StyleFormMixin
from users.models import User
from django import forms
from django.utils.translation import gettext_lazy as _


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class CustomSetPasswordForm(SetPasswordForm):
    """ Переопределяет форму восстановления пароля """

    new_password1 = forms.CharField(
        label=_("Новый пароль "),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Подтверждение нового пароля "),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
