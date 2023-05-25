from django.core.management.base import BaseCommand

from factories import CommentParentFactory, CommentFactory


class Command(BaseCommand):
    help = 'Generate comment'

    def handle(self, *args, **options):
        CommentFactory.create_batch(size=50)
        CommentParentFactory.create_batch(size=100)
        self.stdout.write(self.style.SUCCESS('Successfully generated comment.'))
