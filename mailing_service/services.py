import datetime

from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from mailing_service.models import AttemptMailing


class MailingService:

    @staticmethod
    def start_mailing(mailing):
        mailing.start_time = datetime.datetime.now()
        mailing.status = "launched"
        mailing.save()

        title = mailing.message.title
        content = mailing.message.content
        clients = [client.email for client in mailing.clients.all()]

        for client in clients:
            try:

                send_mail(
                    subject=title,
                    message=content,
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[
                        client,
                    ],
                )

            except Exception as error_text:
                print(str(error_text))
                mailing_attempt = AttemptMailing.objects.create(
                    status="unsuccessfully", server_response=error_text, mailing=mailing
                )
                mailing_attempt.save()
                mailing.status = "completed"
                mailing.save()

            #Если рассылка выполнилась удачно, то выполняется следующий код
            mailing_attempt = AttemptMailing.objects.create(
                status="successfully", mailing=mailing
            )
            mailing_attempt.save()
