from django.db import models


class LabDetail(models.Model):
    name = models.CharField(max_length=100)
    email_id = models.CharField(max_length=100)
    address = models.TextField(max_length=300)
    phone_no = models.CharField(max_length=12)
    def __str__(self):
        self.name   

class PatientDetail(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    phone_no = models.CharField(max_length=12)
    address = models.TextField(max_length=300)
    email_id = models.CharField(max_length=100)
    lab_id = models.ForeignKey(LabDetail, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return f"{self.first_name} {self.last_name}"


class TestDetail(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    sample_needed = models.CharField(max_length=100)
    test_type = models.CharField(max_length=100)
    price = models.IntegerField()
    lab_id = models.ForeignKey(LabDetail, on_delete=models.CASCADE)


class BillDetail(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.IntegerField()


class PatientTestDetail(models.Model):
    patient_id = models.ForeignKey(PatientDetail, on_delete=models.CASCADE)
    lab_id = models.ForeignKey(LabDetail, on_delete=models.CASCADE)
    test_id = models.ForeignKey(TestDetail, on_delete=models.CASCADE)
    bill_id = models.ForeignKey(BillDetail, on_delete=models.CASCADE)

    
