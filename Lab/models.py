from django.db import models


class LabDetail(models.Model):
    name = models.CharField(max_length=100, default='')
    email_id = models.CharField(max_length=100, default='')
    address = models.TextField(max_length=300, default='')
    phone_no = models.CharField(max_length=12, default='')
    password = models.TextField(max_length=300, default='')

    def match_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)

    def set_password(self, raw_password):
        from django.contrib.auth.hashers import make_password
        hash_password = make_password(raw_password, None, 'sha1')
        self.password = hash_password

    def __str__(self):
        return self.name


class PatientDetail(models.Model):
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    age = models.IntegerField()
    phone_no = models.CharField(max_length=12, default='')
    gender = models.CharField(max_length=10, default='')
    address = models.TextField(max_length=300, default='')
    email_id = models.CharField(max_length=100, default='')
    lab = models.ForeignKey(LabDetail, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class TestDetail(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    sample_needed = models.CharField(max_length=100)
    test_type = models.CharField(max_length=100)
    price = models.IntegerField()
    lab = models.ForeignKey(LabDetail, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class BillDetail(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.IntegerField()

    def __str__(self):
        return f"{self.id}"


class PatientTestDetail(models.Model):
    patient = models.ForeignKey(PatientDetail, on_delete=models.CASCADE)
    lab = models.ForeignKey(LabDetail, on_delete=models.CASCADE)
    test = models.ForeignKey(TestDetail, on_delete=models.CASCADE)
    bill = models.ForeignKey(BillDetail, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}"
