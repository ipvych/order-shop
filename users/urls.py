from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView

from .views import Register, ThrottledTokenRefreshView, UserInfo

urlpatterns = [
    path('login/', TokenObtainPairView.as_view()),
    path('user/', UserInfo.as_view()),
    path('register/', Register.as_view()),
    path('refresh-token/', ThrottledTokenRefreshView.as_view()),
]
