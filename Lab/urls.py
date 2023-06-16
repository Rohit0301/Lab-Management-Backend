from django.urls import path

from . import views
urlpatterns = [
    path('login/', views.LabLoginAPIView.as_view(), name="Lab Login"),
    path('register/', views.LabRegistrationAPIView.as_view(),
         name='Lab Registration'),
    path('fetch/<pk>/', views.FetchLabAPIView.as_view(), name="Fetch lab details"),
    path('test/mutate/<pk>/', views.TestAPIView.as_view(),
         name="Add or update test"),
    path('test/fetch/',
         views.TestFetchAPIView.as_view(), name="Fetch Lab Test"),
    path('test/search/', views.FetchTestsByName.as_view(), name="search test"),
    path('patient/search/', views.FetchPatientByEmailID.as_view(),
         name="Search Patient"),
    path('patient/fetch/', views.PatientFetchAPIView.as_view(),
         name="Fetch Lab Patients"),
    path('patient/mutate/<pk>/', views.PatientAPIView.as_view(),
         name="Mutate Lab Patient"),
    path('patient/assign/', views.PatientAssignTestAPIView.as_view(),
         name="Assign test to patient"),
    path('patient/reports/',
         views.PatientReports.as_view(), name="Patient reports")
]
