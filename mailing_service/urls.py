from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import cache_page

from mailing_service.apps import MailingServiceConfig


app_name = MailingServiceConfig.name

urlpatterns = [
    # path("", home, name="home"),
]
