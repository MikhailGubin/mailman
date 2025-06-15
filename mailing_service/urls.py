from django.urls import path
from django.views.decorators.cache import cache_page

from mailing_service.apps import MailingServiceConfig
from mailing_service.views import (AttemptMailingDetailView,
                                   AttemptMailingListView, ClientCreateView,
                                   ClientDeleteView, ClientDetailView,
                                   ClientListView, ClientUpdateView, IndexView,
                                   MailingCompletedView, MailingCreateView,
                                   MailingDeleteView, MailingDetailView,
                                   MailingListView, MailingUpdateView,
                                   MessageCreateView, MessageDeleteView,
                                   MessageDetailView, MessageListView,
                                   MessageUpdateView, SendMessageView)

app_name = MailingServiceConfig.name

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("clients/", ClientListView.as_view(), name="clients_list"),
    path(
        "client/<int:pk>/",
        cache_page(60)(ClientDetailView.as_view()),
        name="client_detail",
    ),
    path("client/new/", ClientCreateView.as_view(), name="client_create"),
    path("client/<int:pk>/edit/", ClientUpdateView.as_view(), name="client_edit"),
    path("client/<int:pk>/delete/", ClientDeleteView.as_view(), name="client_delete"),
    path("messages/", MessageListView.as_view(), name="messages_list"),
    path(
        "message/<int:pk>/",
        cache_page(60)(MessageDetailView.as_view()),
        name="message_detail",
    ),
    path("message/new/", MessageCreateView.as_view(), name="message_create"),
    path("message/<int:pk>/edit/", MessageUpdateView.as_view(), name="message_edit"),
    path(
        "message/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"
    ),
    path("mailings/", MailingListView.as_view(), name="mailings_list"),
    path(
        "mailing/<int:pk>/",
        cache_page(60)(MailingDetailView.as_view()),
        name="mailing_detail",
    ),
    path("mailing/new/", MailingCreateView.as_view(), name="mailing_create"),
    path("mailing/<int:pk>/edit/", MailingUpdateView.as_view(), name="mailing_edit"),
    path(
        "mailing/<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"
    ),
    path(
        "mailing/<int:pk>/send_message/", SendMessageView.as_view(), name="send_message"
    ),
    path("attempts/", AttemptMailingListView.as_view(), name="attempt_list"),
    path(
        "attempt/<int:pk>/",
        cache_page(60)(AttemptMailingDetailView.as_view()),
        name="attempt_detail",
    ),
    path(
        "mailing_completed/<int:pk>/delete/",
        MailingCompletedView.as_view(),
        name="mailing_completed",
    ),
]
