# Generated by Django 4.2.2 on 2025-06-14 17:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("mailing_service", "0014_attemptmailing_owner_client_owner_message_owner"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="attemptmailing",
            options={
                "ordering": ["created_at", "mailing", "status", "server_response"],
                "permissions": [
                    ("can_view_attempt_mailing", "Can view attempt mailing")
                ],
                "verbose_name": "попытка рассылки",
                "verbose_name_plural": "попытки рассылки",
            },
        ),
        migrations.AlterModelOptions(
            name="client",
            options={
                "ordering": ["full_name"],
                "permissions": [("can_view_client", "Can view client")],
                "verbose_name": "клиент",
                "verbose_name_plural": "клиенты",
            },
        ),
        migrations.AlterModelOptions(
            name="mailing",
            options={
                "ordering": ["created_at", "finished_at", "status", "owner", "message"],
                "permissions": [
                    ("can_view_mailing", "Can view mailing"),
                    ("can_edit_status", "Can edit status"),
                ],
                "verbose_name": "рассылка",
                "verbose_name_plural": "рассылки",
            },
        ),
        migrations.AlterModelOptions(
            name="message",
            options={
                "ordering": ["title"],
                "permissions": [("can_view_message", "Can view message")],
                "verbose_name": "сообщение",
                "verbose_name_plural": "сообщения",
            },
        ),
        migrations.RemoveField(
            model_name="client",
            name="owner",
        ),
        migrations.AddField(
            model_name="client",
            name="manager",
            field=models.ForeignKey(
                blank=True,
                help_text="Укажите менеджера клиента",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Менеджер клиента",
            ),
        ),
        migrations.AlterField(
            model_name="mailing",
            name="message",
            field=models.ForeignKey(
                blank=True,
                help_text="Укажите сообщение",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="mailing_service.message",
                verbose_name="Сообщение",
            ),
        ),
    ]
