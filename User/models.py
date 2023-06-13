from django.db import models


class UserDetail(models.Model):
    full_name = models.CharField(max_length=100, default='')
    email_id = models.CharField(max_length=100, default='')
    password = models.TextField(max_length=300, default='')

    def match_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)

    def set_password(self, raw_password):
        from django.contrib.auth.hashers import make_password
        hash_password = make_password(raw_password, None, 'sha1')
        self.password = hash_password

    def __str__(self):
        return self.full_name
