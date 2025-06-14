import secrets
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetConfirmView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from config.settings import EMAIL_HOST_USER

from .forms import UserRegisterForm, CustomSetPasswordForm, UserForm
from .models import User
from django.views.generic import DetailView, ListView



class UserCreateView(CreateView):
    """ Создание пользователя """
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        """" Регистрация пользователя """
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Добро пожаловать в наш сервис",
            message=f"Спасибо, что зарегистрировались в нашем сервисе! "
            f"Для подтверждения почты необходимо пройти по ссылке {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    """ Подтверждение регистрации пользователя """
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class UserListView(ListView):
    """Класс для представления объектов класса 'Пользователь'"""

    model = User
    context_object_name = "users"


class UserDetailView(LoginRequiredMixin, DetailView):
    """Выводит представление отдельного объекта класса 'Клиент'"""

    model = User
    context_object_name = "user"


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Создаёт представление объекта класса 'Клиент'"""

    model = User
    form_class = UserForm
    success_url = reverse_lazy("users:users_list")


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """ Подтверждение нового пароля """
    form_class = CustomSetPasswordForm
