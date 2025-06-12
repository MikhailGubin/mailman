from django.db import models
from django.db.models import ForeignKey

from users.models import User


class Client(models.Model):
    """Модель 'Клиент'"""

    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(
        max_length=150,
        verbose_name="Ф.И.О.",
        help_text="Введите полное Ф.И.О. клиента",
    )
    comment = models.TextField(
        verbose_name="Комментарий",
        help_text="Введите комментарий",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"
        ordering = ["full_name"]


class Message(models.Model):
    """Модель 'Сообщение'"""

    title = models.CharField(
        max_length=150, verbose_name="Тема письма", help_text="Введите тему письма"
    )
    content = models.TextField(
        verbose_name="Содержимое письма",
        help_text="Введите содержимое письма",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"
        ordering = ["title"]


class Mailing(models.Model):
    """Модель 'Рассылка'"""

    STATUS_OPTIONS = (
        ("completed", "Завершена"),
        ("created", "Создана"),
        ("launched", "Запущена"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата регистрации продукта",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата последнего изменения информации о продукте",
    )
    status = models.CharField(max_length=10, choices=STATUS_OPTIONS, default="created")
    message = models.ForeignKey(
        Message,
        verbose_name="Сообщение",
        help_text="Укажите сообщение",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    clients = models.ManyToManyField(
        Client,
        verbose_name="Клиенты",
        help_text="Укажите клиентов рассылки",
        blank=True,
    )
    owner = models.ForeignKey(
        User,
        verbose_name="Автор рассылки",
        help_text="Укажите автора рассылки",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"Рассылка создана {self.created_at} автором - {self.owner} "

    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"
        ordering = ["created_at", "updated_at", "status", "owner", "message"]
