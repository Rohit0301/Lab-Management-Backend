from django.contrib import admin
from .models import LabDetail, PatientDetail, TestDetail, BillDetail, PatientTestDetail
# Register your models here.
labModels = [LabDetail, PatientDetail, TestDetail, BillDetail, PatientTestDetail]
admin.site.register(labModels)