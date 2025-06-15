import datetime
from django.db import models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.views.generic import CreateView, ListView
from django.core.cache import cache
from config.settings import EMAIL_HOST_USER, CACHE_ENABLED
from mailing_service.models import AttemptMailing


class MailingService:

    @staticmethod
    def start_mailing(mailing, user):
        mailing.start_time = datetime.datetime.now()
        mailing.status = "launched"
        mailing.save()

        title = mailing.message.title
        content = mailing.message.content
        clients = [client.email for client in mailing.clients.all()]

        for client in clients:

            try:
                if "@test.ru" in client.email:
                    raise Exception("Не правильно указана почта клиента")

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
                    status="unsuccessfully", server_response=error_text, mailing=mailing,
                    owner=user
                )
                mailing_attempt.save()
                mailing.status = "completed"
                mailing.save()

            # Если рассылка выполнилась удачно, то выполняется следующий код
            mailing_attempt = AttemptMailing.objects.create(
                status="successfully", mailing=mailing
            )
            mailing_attempt.save()

    @staticmethod
    def get_from_cache(custom_model):
        """Получает данные по продуктам из кэша. Если кэш пуст, получает данные из БД"""
        if not CACHE_ENABLED:
            return custom_model.objects.all()
        key = "operand_list"
        operands = cache.get(key)
        if operands is not None:
            return operands
        operands = custom_model.objects.all()
        cache.set(key, operands, 60)
        return operands


class CustomCreateView(LoginRequiredMixin, CreateView):
    """Шаблон для создания представления объекта нужного класса """

    def form_valid(self, form):
        object = form.save()
        user = self.request.user
        object.owner = user
        object.save()
        return super().form_valid(form)


class CustomListView(ListView):
    """Класс для представления объектов нужного класса """

    model = models.Model

    def get_queryset(self):
        """
        Выводит на экран все объекты, если пользователь является Менеджером.
        В противном случае выводит только те объекты, которые создал данный Пользователь.
        """
        user = self.request.user
        permissions = [user.has_perm("mailing_service.can_view_client"),
                       user.has_perm("mailing_service.can_view_message"),
                       user.has_perm('mailing_service.can_view_mailing'),
                       user.has_perm('mailing_service.can_edit_status'),
                       user.has_perm('mailing_service.can_view_attempt_mailing')]

        if all(permissions):
            return self.model.objects.all()[0:9]

        return self.model.objects.all().filter(owner=self.request.user)[0:9]
