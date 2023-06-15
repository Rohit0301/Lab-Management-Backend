from django.urls import path

from . import views
urlpatterns = [
    path('login/', views.LabLoginAPIView.as_view(), name="Lab Login"),
    path('register/', views.LabRegistrationAPIView.as_view(),
         name='Lab Registration'),
    path('fetch/<pk>/', views.FetchLabAPIView.as_view(), name="Fetch lab details"),
    path('test/mutate/<pk>/', views.TestAPIView.as_view()),
    path('test/fetch/<lab_id>/',
         views.TestFetchAPIView.as_view(), name="Fetch Lab Test"),
    path('patient/fetch/<lab_id>/', views.PatientFetchAPIView.as_view(),
         name="Fetch Lab Patients"),
    path('patient/mutate/<pk>/', views.PatientAPIView.as_view(),
         name="Mutate Lab Patient"),
    path('patient/assign/<lab_id>/', views.PatientAssignTestAPIView.as_view(),
         name="Assign test to patient"),
    path('patient/reports/',
         views.PatientReports.as_view(), name="Patient reports")
    #     path('test/create/', views.TestCreateAPIView.as_view(), name="Lab Test"),
    #     path('test/update/<test_id>/',
    #          views.TestUpdateAPIView.as_view(), name="Test Update or delete"),
    #     path('test/fetch/<lab_id>/', views.TestFetchAPIView.as_view(),
    #          name="Fetch Lab Tests"),
    #     path('patient/<lab_id>/', views.PatientAPIView.as_view(),
    #          name="Patient Registration"),
    #     path('patient/update/<patient_id>/',
    #          views.PatientUpdateAPIView.as_view(), name="Patient update or delete"),
]
