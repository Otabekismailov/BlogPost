from django.urls import path

from .views import PostListApiView, PostDetailApiView, PostLikeApiView, AddCommentAPI, CategoryListApi, \
    LikeDislikeListApi

urlpatterns = [
    path('', PostListApiView.as_view(), name='post-list'),
    path('<slug:slug>', PostDetailApiView.as_view(), name='post-detail'),
    path('likedislike/', LikeDislikeListApi.as_view(), name='like_dislike-list'),
    path('<slug:slug>/likedislike/', PostLikeApiView.as_view(), name='like_dislike'),
    path('blog/<slug:slug>/comment/', AddCommentAPI.as_view(), name='comment-add'),
    path('category/', CategoryListApi.as_view(), name='category-list')
]
