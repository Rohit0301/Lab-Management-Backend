from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.UserLoginAPIView.as_view(), name="User Login"),
    path('register/', views.UserRegistrationAPIView.as_view(), name="User Register")
]
