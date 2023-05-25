from django.core.management.base import BaseCommand

from factories import CategoryFactory


class Command(BaseCommand):
    help = 'Generate category'

    def handle(self, *args, **options):
        CategoryFactory.create_batch(size=20)
        self.stdout.write(self.style.SUCCESS('Successfully generated category.'))
