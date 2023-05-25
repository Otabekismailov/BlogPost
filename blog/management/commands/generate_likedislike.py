from django.core.management import BaseCommand

from factories import LikeDisLikeFactory


class Command(BaseCommand):
    help = 'Generate like_dislike'

    def handle(self, *args, **options):
        LikeDisLikeFactory.create_batch(size=100)
        self.stdout.write(self.style.SUCCESS('Successfully generated like_dislike.'))
