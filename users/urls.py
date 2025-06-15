from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetCompleteView, PasswordResetConfirmView
from django.urls import path, reverse_lazy

from users.apps import UsersConfig
from users.views import UserCreateView, email_verification, UserListView, \
    UserDetailView, UserUpdateView, UserBlockView

app_name = UsersConfig.name


urlpatterns = [
                  path("login/", LoginView.as_view(template_name="login.html"), name="login"),
                  path("logout/", LogoutView.as_view(), name="logout"),
                  path("register/", UserCreateView.as_view(), name="register"),
                  path("", UserListView.as_view(), name="users_list"),
                  path("<int:pk>/", UserDetailView.as_view(), name="user_detail"),
                  path("<int:pk>/edit/", UserUpdateView.as_view(), name="user_edit"),
                  path("<int:pk>/user_block/", UserBlockView.as_view(), name="user_block"),
                  path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
                  path('password-reset/',
                       PasswordResetView.as_view(
                           template_name="users/password_reset_form.html",
                           email_template_name="users/password_reset_email.html",
                           success_url=reverse_lazy("users:password_reset_done")
                       ),
                       name='password_reset'),
                  path('password-reset/done/',
                       PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
                       name='password_reset_done'),
                  path('password-reset/<uidb64>/<token>/',
                       PasswordResetConfirmView.as_view(
                           template_name="users/password_reset_confirm.html",
                           success_url=reverse_lazy("users:password_reset_complete")
                       ),
                       name='password_reset_confirm'),
                  path('password-reset/complete/',
                       PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
                       name='password_reset_complete'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
