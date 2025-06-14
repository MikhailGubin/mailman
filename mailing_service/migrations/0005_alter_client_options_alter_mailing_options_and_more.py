# Generated by Django 4.2.2 on 2025-06-12 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailing_service", "0004_rename_mailings_mailing"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="client",
            options={
                "ordering": ["full_name"],
                "verbose_name": "клиент",
                "verbose_name_plural": "клиенты",
            },
        ),
        migrations.AlterModelOptions(
            name="mailing",
            options={
                "ordering": ["created_at", "updated_at", "status", "owner", "message"],
                "verbose_name": "рассылка",
                "verbose_name_plural": "рассылки",
            },
        ),
        migrations.RemoveField(
            model_name="mailing",
            name="client",
        ),
        migrations.AddField(
            model_name="mailing",
            name="clients",
            field=models.ManyToManyField(
                blank=True,
                help_text="Укажите клиента",
                to="mailing_service.client",
                verbose_name="Клиент",
            ),
        ),
        migrations.AlterField(
            model_name="client",
            name="full_name",
            field=models.CharField(
                help_text="Введите полное Ф.И.О. клиента",
                max_length=150,
                verbose_name="Ф.И.О.",
            ),
        ),
    ]
