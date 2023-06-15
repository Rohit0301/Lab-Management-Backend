from django.urls import path
from . import views

urlpatterns = [
    path('fetch/',
         views.FetchUserBySessionId.as_view(), name="Fetch user"),
    path('logout/', views.SessionLogoutView.as_view(), name="logout")
]
