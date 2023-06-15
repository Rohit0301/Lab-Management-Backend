from django.db import models

# Create your models here.


class Session(models.Model):
    session_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=50)
    user_id = models.IntegerField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.session_id
