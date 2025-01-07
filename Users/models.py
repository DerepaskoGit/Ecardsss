from django.db import models
from django.contrib.auth.models import User

class InviteCodeDb(models.Model):
    invite_code = models.CharField(max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='invite_code')

    def __str__(self):
        return self.invite_code
