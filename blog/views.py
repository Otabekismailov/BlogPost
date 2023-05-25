from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, \
    RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Comment, Post, LikeDislike, Category, Tag
from blog.serializers import AddCommentSerializer, PostApiListSerializers, PostApiCreateSerializers, \
    PostLikeDislikeSerializer, CategoryListSerializers, PostLikeDislikeListSerializer, TagSerializers
from paginations import CustomPageNumberPagination


class PostListApiView(ListCreateAPIView):
    queryset = Post.objects.order_by('-like_dislike')
    permission_classes = (AllowAny,)
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = ("category", "tag")
    ordering_fields = ("likes", "dislikes")
    search_fields = ("title", "category__name", "tag__name",)

    def get_permissions(self):
        if self.request.method == SAFE_METHODS or self.request.method == "GET":
            self.permission_classes = (AllowAny,)
            self.serializer_class = PostApiListSerializers
            return [permission() for permission in self.permission_classes]
        self.permission_classes = (IsAuthenticated,)
        self.serializer_class = PostApiCreateSerializers
        return [permission() for permission in self.permission_classes]

    def get_serializer(self, *args, **kwargs):
        if self.request.method == "POST":
            self.permission_classes = (IsAuthenticated,)
            serializer_class = PostApiCreateSerializers
            kwargs.setdefault('context', self.get_serializer_context())
            return serializer_class(*args, **kwargs)
        else:
            self.permission_classes = (AllowAny,)
            serializer_class = PostApiListSerializers
            kwargs.setdefault('context', self.get_serializer_context())
            return serializer_class(*args, **kwargs)

    def perform_create(self, serializers):
        serializers.save(author=self.request.user)


class PostDetailApiView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostApiListSerializers
    pagination_class = CustomPageNumberPagination
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            reviewed = self.queryset.values('reviewed').get(slug=self.kwargs.get('slug'))
            reviews = reviewed.get("reviewed")
            reviews += 1
            self.queryset.values('reviewed').filter(slug=self.kwargs.get('slug')).update(reviewed=reviews)

            return self.retrieve(request, *args, **kwargs)

    def get_permissions(self):
        if self.request.method == SAFE_METHODS:
            self.permission_classes = (AllowAny,)
            self.serializer_class = PostApiListSerializers
            return [permission() for permission in self.permission_classes]
        return [permission() for permission in self.permission_classes]


class AddCommentAPI(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = AddCommentSerializer
    permission_class = (IsAuthenticated,)
    lookup_field = 'slug'

    def perform_create(self, serializers):
        slug = self.kwargs.get('slug')
        post = get_object_or_404(Post, slug=slug)
        serializers.save(post=post, author=self.request.user)


class CommentDetailApi(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = AddCommentSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            pk = self.kwargs.get("pk")
            comment = get_object_or_404(Comment, pk=pk)
            if comment:
                reviewed = self.queryset.values('reviewed').get(pk=pk)
                reviews = reviewed.get("reviewed")
                reviews += 1
                self.queryset.values('reviewed').filter(pk=pk).update(reviewed=reviews)
        return self.retrieve(request, *args, **kwargs)


class PostLikeApiView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=PostLikeDislikeSerializer)
    def post(self, request, *args, **kwargs):
        serializer = PostLikeDislikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        type_ = serializer.validated_data.get("type")
        user = request.user
        post = Post.objects.filter(slug=self.kwargs.get("slug")).first()
        if not post:
            raise Http404
        like = LikeDislike.objects.all()
        if like.filter(type=type_):
            like.delete()
            data = {"type": type_, "detail": "delete."}
            return Response(data)

        else:
            LikeDislike.objects.update_or_create(post=post, user=user, defaults={"type": type_})
            if type_ == 1:
                data = {"type": type_, "detail": "Liked."}
                return Response(data)
            elif type_ == -1:
                data = {"type": type_, "detail": "DisLiked."}
                return Response(data)


class LikeDislikeListApi(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPageNumberPagination
    serializer_class = PostLikeDislikeListSerializer
    queryset = LikeDislike.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = get_object_or_404(self.queryset, user_id=request.user.id)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class CategoryListApi(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializers
    pagination_class = CustomPageNumberPagination
    permission_classes = (AllowAny,)


class TagListApi(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers
    permission_classes = (AllowAny,)
    pagination_class = CustomPageNumberPagination
