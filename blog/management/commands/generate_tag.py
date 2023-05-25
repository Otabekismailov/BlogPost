from django.core.management.base import BaseCommand

from factories import TagFactory


class Command(BaseCommand):
    help = 'Generate tag'

    def handle(self, *args, **options):
        TagFactory.create_batch(size=100)
        self.stdout.write(self.style.SUCCESS('Successfully generated tag.'))
