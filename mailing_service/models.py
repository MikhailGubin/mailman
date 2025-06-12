from django.db import models
from django.db.models import ForeignKey

from users.models import User


class Addressee(models.Model):
    """  Модель 'Получатель рассылки' """
    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(max_length=150, verbose_name="Ф.И.О.",
                                 help_text="Введите полное Ф.И.О. получателя рассылки"
                                 )
    comment = models.TextField(verbose_name="Комментарий", help_text="Введите комментарий",
                               blank=True,null=True,
                               )

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"
        ordering = ["full_name"]
