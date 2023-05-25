from django.core.management.base import BaseCommand

from factories import PostFactory

class Command(BaseCommand):
    help = 'Generate post'

    def handle(self, *args, **options):

        PostFactory.create_batch(size=100)
        self.stdout.write(self.style.SUCCESS('Successfully generated post.'))
