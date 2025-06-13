from django.contrib import admin
from django.contrib.admin import ModelAdmin

from mailing_service.models import Client, Message, Mailing, AttemptMailing


@admin.register(Client)
class ClientAdmin(ModelAdmin):
    list_display = ["email", "comment"]
    list_filter = ("email",)
    search_fields = ( "email", "comment",)


@admin.register(Message)
class MessageAdmin(ModelAdmin):
    list_display = ["title", "content"]
    list_filter = ("title",)
    search_fields = ("title","content",)


@admin.register(Mailing)
class MailingAdmin(ModelAdmin):
    list_display = ["status", "message", "owner"]
    list_filter = ("status", "message", "clients", "owner")
    search_fields = ("status", "message", "clients", "owner")


@admin.register(AttemptMailing)
class AttemptMailingAdmin(ModelAdmin):
    list_display = ["status", "server_response", "mailing", "created_at"]
    list_filter = ("status", "server_response", "created_at",)
    search_fields = ("status", "server_response", "created_at", "mailing")
