from django.urls import path
from core.views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login',  UserLoginView.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', UserRegisterView.as_view(), name="sign_up"),
]