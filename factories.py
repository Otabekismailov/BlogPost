import factory
from faker import Faker
import factory.fuzzy

from blog.models import LikeDislike


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'users.User'
        django_get_or_create = ['username']

    email = factory.Faker("email")
    username = factory.Faker("first_name")
    password = factory.Faker("password")


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'blog.Tag'
        django_get_or_create = ['name']

    name = factory.Faker("company")


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'blog.Category'
        django_get_or_create = ['name']

    name = factory.Faker("word")


# class ParentPostFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = 'blog.Post'
#         django_get_or_create = ['category']
#
#     title = factory.Faker("sentence")
#     tag = factory.SubFactory(TagFactory)
#     category = factory.SubFactory(CategoryFactory)
#     text = factory.Faker("text")
#     author = factory.SubFactory(UserFactory)


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'blog.Post'
        django_get_or_create = ['category', 'tag']

    title = factory.Faker("sentence")
    tag = factory.SubFactory(TagFactory)
    category = factory.SubFactory(CategoryFactory)
    text = factory.Faker("text")
    author = factory.SubFactory(UserFactory)
    reviewed = factory.Faker("pyint")


class CommentParentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'blog.Comment'
        django_get_or_create = ['post', 'author']

    content = factory.Faker("text")
    post = factory.SubFactory(PostFactory)
    author = factory.SubFactory(UserFactory)
    reviewed = factory.Faker("pyint")
    is_active = factory.Faker("True").provider


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'blog.Comment'
        django_get_or_create = ['post', 'author']

    content = factory.Faker("emoji")
    post = factory.SubFactory(PostFactory)
    author = factory.SubFactory(UserFactory)
    parent = factory.SubFactory(CommentParentFactory)


LikeDislikeType = [x[0] for x in LikeDislike.LikeType.choices]


class LikeDisLikeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'blog.LikeDislike'

    post = factory.SubFactory(PostFactory)
    user = factory.SubFactory(UserFactory)
    type = factory.fuzzy.FuzzyChoice(LikeDislikeType)
