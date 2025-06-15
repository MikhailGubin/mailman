from django.db import models

from users.models import User


class Client(models.Model):
    """Модель 'Клиент'"""

    email = models.EmailField(max_length=50, unique=True, verbose_name="Email")
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
    owner = models.ForeignKey(
        User,
        verbose_name="Менеджер клиента",
        help_text="Укажите менеджера клиента",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"
        ordering = ["full_name"]
        permissions = [
            ("can_view_client", "Can view client"),
        ]


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
    owner = models.ForeignKey(
        User,
        verbose_name="Автор сообщения",
        help_text="Укажите автора сообщения",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"
        ordering = ["title"]
        permissions = [
            ("can_view_message", "Can view message"),
        ]


class Mailing(models.Model):
    """Модель 'Рассылка'"""

    STATUS_OPTIONS = (
        ("completed", "Завершена"),
        ("created", "Создана"),
        ("launched", "Запущена"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время создания рассылки",
    )
    finished_at = models.DateTimeField(
        verbose_name="Дата и время окончания рассылки",
        null=True,
        blank=True,
    )
    status = models.CharField(max_length=10, choices=STATUS_OPTIONS, default="created")
    message = models.ForeignKey(
        Message,
        verbose_name="Сообщение",
        help_text="Укажите сообщение",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
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
        ordering = ["created_at", "finished_at", "status", "owner", "message"]
        permissions = [
            ("can_view_mailing", "Can view mailing"),
            ("can_edit_status", "Can edit status"),
        ]


class AttemptMailing(models.Model):
    """Модель 'Попытка рассылки'"""

    STATUS_OPTIONS = (
        ("successfully", "Успешно"),
        ("unsuccessfully", "Не успешно"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время попытки рассылки",
    )
    status = models.CharField(
        max_length=15, choices=STATUS_OPTIONS, default="successfully"
    )
    server_response = models.TextField(
        verbose_name="Ответ почтового сервера",
        blank=True,
        null=True,
    )
    mailing = models.ForeignKey(
        Mailing,
        verbose_name="Рассылка",
        help_text="Укажите рассылку",
        on_delete=models.CASCADE,
    )
    owner = models.ForeignKey(
        User,
        verbose_name="Автор рассылки",
        help_text="Укажите автора рассылки",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "попытка рассылки"
        verbose_name_plural = "попытки рассылки"
        ordering = ["created_at", "mailing", "status", "server_response"]
        permissions = [
            ("can_view_attempt_mailing", "Can view attempt mailing"),
        ]

    def __str__(self):
        return f"Рассылка запущена {self.created_at} автором - {self.owner}. Статус -  {self.status}."
