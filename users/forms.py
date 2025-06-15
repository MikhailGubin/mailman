from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import SetPasswordForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from mixin_form import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Форма для регистрации Пользователя"""

    class Meta:
        model = User
        fields = ("email", "password1", "password2")


# class CustomSetPasswordForm(SetPasswordForm):
#     """ Переопределяет форму восстановления пароля """
#
#     new_password1 = forms.CharField(
#         label=_("Новый пароль "),
#         widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
#         strip=False,
#         help_text=password_validation.password_validators_help_text_html(),
#     )
#     new_password2 = forms.CharField(
#         label=_("Подтверждение нового пароля "),
#         strip=False,
#         widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
#     )


class UserForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = User
        fields = (
            "email",
            "phone_number",
            "avatar",
            "country",
        )
