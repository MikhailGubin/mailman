import secrets
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from config.settings import EMAIL_HOST_USER

from .forms import UserRegisterForm, UserForm
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
    context_object_name = "users_profile_list"

    def get_queryset(self):
        """Определяет логику вывода на экран списка Пользователей"""

        user = self.request.user
        if user.has_perm("users.can_edit_is_active") and user.has_perm("users.can_view_user"):
            return User.objects.all()

        return User.objects.filter(pk=self.request.user.pk)


class UserDetailView(LoginRequiredMixin, DetailView):
    """Выводит представление отдельного объекта класса 'Клиент'"""

    model = User
    context_object_name = "user_profile"


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Создаёт представление объекта класса 'Клиент'"""

    model = User
    form_class = UserForm
    success_url = reverse_lazy("users:users_list")

    # def get_form_class(self):
    #     """ Определяет права доступа для редактирования профиля Пользователя """
    #     user = self.request.user
    #     user_profile = self.object
    #     if user_profile.pk == user.pk:
    #         return UserForm
    #     elif user.has_perm("users.can_edit_is_active") and user.has_perm("users.can_view_user"):
    #         return ManagerForm
    #
    #     raise PermissionDenied


class UserBlockView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy("mailing_service:mailings_list")
    template_name = "users/confirm_user_block.html"

    def post(self, request, pk):
        user_to_block = get_object_or_404(User, pk=pk)
        user = self.request.user

        if not request.user.has_perm("users.can_edit_is_active"):
            return HttpResponseForbidden(
                "У вас нет прав для блокировки Пользователя"
            )
        elif user.pk == user_to_block.pk:
            return HttpResponseForbidden(
                "Нельзя себя заблокировать"
            )

        user_to_block.is_active = False
        user_to_block.save()

        return redirect("users:users_list")


# class CustomPasswordResetConfirmView(PasswordResetConfirmView):
#     """ Подтверждение нового пароля """
#     form_class = CustomSetPasswordForm
