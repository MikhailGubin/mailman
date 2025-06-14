import os

from django.core.management import BaseCommand
from dotenv import load_dotenv

from users.models import User

# Загружаем переменные окружения из файла .env
load_dotenv()


class Command(BaseCommand):
    """Создаёт суперпользователя"""

    def handle(self, *args, **options):
        user = User.objects.create(email=os.getenv("ADMIN_EMAIL"))
        user.set_password(os.getenv("ADMIN_PASSWORD"))
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
