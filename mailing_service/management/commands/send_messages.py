import os

from django.core.mail import send_mail
from django.core.management import call_command
from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from mailing_service.models import Mailing

from config.settings import EMAIL_HOST_USER


class Command(BaseCommand):
    help = "Отправляет сообщения клиентам из рассылки с pk=4"

    def handle(self, *args, **kwargs):

        mailing = get_object_or_404(Mailing, pk=4)
        title = mailing.message.title
        content = mailing.message.content
        clients = [client.email for client in mailing.clients.all()]

        for client in clients:
            send_mail(
                subject=title,
                message=content,
                from_email=EMAIL_HOST_USER,
                recipient_list=[client, ],
            )

        # # Удаляем существующие записи
        # Product.objects.all().delete()
        # Category.objects.all().delete()
        #
        # call_command("loaddata", "category_fixture.json")
        # self.stdout.write(
        #     self.style.SUCCESS("Successfully loaded data from category_fixture.json")
        # )
        #
        # call_command("loaddata", "product_fixture.json")
        # self.stdout.write(
        #     self.style.SUCCESS("Successfully loaded data from product_fixture.json")
        # )