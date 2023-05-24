import datetime

from django.db import models
from django.utils.functional import cached_property
from django.utils.text import slugify, gettext_lazy as _

from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.name.upper():
            self.slug = slugify(self.name.lower())
        self.slug = slugify(self.name.lower())
        return super().save(force_insert, force_update, using, update_fields)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.name.upper():
            self.slug = slugify(self.name.lower())
        self.slug = slugify(self.name)
        return super().save(force_insert, force_update, using, update_fields)


# Create your models here.
class Post(models.Model):
    tag = models.ForeignKey(Tag, related_name='post', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    author = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    pub_year = datetime.datetime.now().strftime("%H:%M / %d.%m.%Y")
    video = models.FileField(upload_to='video', null=True, blank=True)
    reviewed = models.IntegerField(default=0)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, related_name="post")

    def __str__(self):
        return self.title

    @property
    def likes(self):
        return self.like_dislike.filter(type=LikeDislike.LikeType.LIKE).count()

    @property
    def dislikes(self):
        return self.like_dislike.filter(type=LikeDislike.LikeType.DISLIKE).count()

    def save(self, *args, **kwargs):
        if self.title.upper():
            self.slug = slugify(self.title.lower())
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    is_active = models.BooleanField(default=False)
    reviewed = models.IntegerField(default=0)

    def __str__(self):
        return f'Comment by {self.author.email} on {self.post}'

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

    class Meta:
        ordering = ('created_at',)


class LikeDislike(models.Model):
    class LikeType(models.IntegerChoices):
        LIKE = 1, _("like")
        DISLIKE = -1, _("dislike")

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like_dislike')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="like_dislike")
    type = models.CharField(choices=LikeType.choices)

    def __str__(self):
        if self.type == '1':
            return f'Like  by {self.user.email} on {self.post}'
        elif self.type == '-1':
            return f'DisLike  by {self.user.email} on {self.post}'

    class Meta:
        unique_together = ['post', 'user']
