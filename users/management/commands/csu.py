from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):

        # User.objects.all().delete()

        user = User.objects.create(email='q')
        user.set_password('q')
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
