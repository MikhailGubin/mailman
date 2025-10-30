from django.core.mail import send_mail
from django.core.management import BaseCommand

from config.settings import EMAIL_HOST_USER
from mailing_service.models import Mailing


class Command(BaseCommand):
    help = (
        "Отправляет сообщения клиентам из рассылок со статусами 'Создана' и 'Запущена' "
    )

    def handle(self, *args, **kwargs):

        active_mailings = [
            mailing
            for mailing in Mailing.objects.all()
            if mailing.status in ["launched", "created"]
        ]
        for mailing in active_mailings:
            title = mailing.message.title
            content = mailing.message.content
            clients = [client.email for client in mailing.clients.all()]

            for client in clients:
                send_mail(
                    subject=title,
                    message=content,
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[
                        client,
                    ],
                )
