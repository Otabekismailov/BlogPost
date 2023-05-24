from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Comment, Post, LikeDislike, Category
from blog.serializers import AddCommentSerializer, PostApiListSerializers, PostApiCreateSerializers, \
    PostLikeDislikeSerializer, CategoryListSerializers, PostLikeDislikeListSerializer
from paginations import CustomPageNumberPagination


class PostListApiView(ListCreateAPIView):
    queryset = Post.objects.order_by("like_dislike")
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = ("category", "tag")
    ordering_fields = ("likes", "dislikes")
    search_fields = ("title", "category__name", "tag__name",)

    def get_serializer_class(self):
        if self.request.method == "POST":
            if self.request.user.is_anonymous:
                data = {"detail": self.request.user.is_anonymous}
                return Response(data, status=status.HTTP_401_UNAUTHORIZED)

            return PostApiCreateSerializers
        elif self.request.method == "GET":
            return PostApiListSerializers

    def perform_create(self, serializers):
        serializers.save(author=self.request.user)


class PostDetailApiView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostApiListSerializers
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            reviewed = self.queryset.values('reviewed').get(slug=self.kwargs.get('slug'))
            reviews = reviewed.get("reviewed")
            reviews += 1
            self.queryset.values('reviewed').filter(slug=self.kwargs.get('slug')).update(reviewed=reviews)
        return self.retrieve(request, *args, **kwargs)


class AddCommentAPI(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = AddCommentSerializer
    permission_class = [IsAuthenticated]
    lookup_field = 'slug'

    def perform_create(self, serializers):
        slug = self.kwargs.get('slug')
        post = get_object_or_404(Post, slug=slug)
        if self.request.method == "GET":
            reviewed = post.objects.values('reviewed').get(slug=slug)
            reviewed += 1
            post.objects.values('reviewed').filter(slug=slug).update(reviewed=reviewed)
        serializers.save(post=post, author=self.request.user)


# def post(request):


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
    queryset = LikeDislike.objects.all()
    serializer_class = PostLikeDislikeListSerializer
    pagination_class = CustomPageNumberPagination


class CategoryListApi(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializers
    pagination_class = CustomPageNumberPagination
