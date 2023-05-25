from django.urls import path, re_path

from .social_user.views import FacebookSocialAuthView, GoogleSocialAuthView
from .views import RegistrationView, LoginView, LogoutView, ChangePasswordView, UserListApi
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('userlist/', UserListApi.as_view(), name='user-list'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/faceobok/', FacebookSocialAuthView.as_view(), name='facebook_login'),
    path('auth/google/', GoogleSocialAuthView.as_view(), name='google_login'),
]
