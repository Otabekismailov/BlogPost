from django.urls import path

from .views import PostListApiView, PostDetailApiView, PostLikeApiView, AddCommentAPI, CategoryListApi, \
    LikeDislikeListApi, CommentDetailApi, TagListApi

urlpatterns = [
    path('post/', PostListApiView.as_view(), name='post-list'),
    path('<slug:slug>', PostDetailApiView.as_view(), name='post-detail'),
    path('likedislike/', LikeDislikeListApi.as_view(), name='like_dislike-list'),
    path('blog/<slug:slug>/likedislike/', PostLikeApiView.as_view(), name='like_dislike'),
    path('blog/<slug:slug>/comment/', AddCommentAPI.as_view(), name='comment-add'),
    path('comment/<int:pk>/', CommentDetailApi.as_view(), name='comment-detail'),
    path('category/', CategoryListApi.as_view(), name='category-list'),
    path('tag/', TagListApi.as_view(), name='tag-list'),
]
