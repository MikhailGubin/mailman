from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import cache_page

from mailing_service.apps import MailingServiceConfig
from mailing_service.views import (ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView,
                                   ClientDeleteView)

app_name = MailingServiceConfig.name

urlpatterns = [
    # path("", home, name="home"),
    path("clients/", ClientListView.as_view(), name="clients_list"),
    path(
        "client/<int:pk>/",
        ClientDetailView.as_view(),
        name="client_detail",
    ),
    path("new/", ClientCreateView.as_view(), name="client_create"),
    path("<int:pk>/edit/", ClientUpdateView.as_view(), name="client_edit"),
    path("<int:pk>/delete/", ClientDeleteView.as_view(), name="client_delete"),

]

