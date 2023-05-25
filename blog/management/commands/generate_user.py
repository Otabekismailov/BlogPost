from django.core.management.base import BaseCommand

from factories import UserFactory


class Command(BaseCommand):
    help = 'Generate user'

    def handle(self, *args, **options):
        UserFactory.create_batch(size=100)
        self.stdout.write(self.style.SUCCESS('Successfully generated user.'))
