from django.core.management import call_command
from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Загружает Пользователей"

    def handle(self, *args, **kwargs):

        # Удаляем существующие записи
        User.objects.all().delete()

        call_command("loaddata", "users_fixture.json")
        self.stdout.write(
            self.style.SUCCESS("Successfully loaded data from users_fixture.json")
        )
