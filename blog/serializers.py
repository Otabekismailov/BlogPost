from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from blog.models import Post, Comment, LikeDislike, Category
from users.models import User


class PostAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email",)


class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug",)


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content', 'reviewed', 'parent',)


class PostApiCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'text', 'tag', 'image', 'video',)


class PostApiListSerializers(serializers.ModelSerializer):
    author = PostAuthorSerializer()
    category = PostCategorySerializer()
    comments = PostCommentSerializer(many=True)

    class Meta:
        model = Post
        fields = (
            'title', 'slug', 'text', 'tag', 'image', 'video', 'category', 'author', 'comments', 'reviewed', 'likes',
            'dislikes',)

        # read_only_fields = ("category", "author",)


class AddCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content', 'post', 'author', 'reviewed', 'parent')
        read_only_fields = ("id", "post", "author", "reviewed",)


class PostLikeDislikeSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=LikeDislike.LikeType.choices)


class PostLikeDislikeListSerializer(serializers.ModelSerializer):
    post = PostApiListSerializers()

    class Meta:
        model = LikeDislike
        fields = ('id', 'type', 'post',)


class CategoryListSerializers(serializers.ModelSerializer):
    post = PostApiListSerializers(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'post')
