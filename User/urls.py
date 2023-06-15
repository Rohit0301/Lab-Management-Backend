from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.UserLoginAPIView.as_view(), name="User Login"),
    path('register/', views.UserRegistrationAPIView.as_view(), name="User Register"),
    path('fetch/<pk>/', views.FetchUserAPIView.as_view(),
         name="Fetch User details"),
    path('reports/', views.FetchUserReportsAPIView.as_view(), name="Fetch Reports")
]
