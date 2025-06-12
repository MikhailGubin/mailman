from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import cache_page

from users.apps import UsersConfig


app_name = UsersConfig.name

urlpatterns = [
    # path("", home, name="home"),
]