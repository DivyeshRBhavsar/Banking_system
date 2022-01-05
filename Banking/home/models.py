from django.db import models
from django.contrib.auth.models import User


class signup(models.Model):
    IR = models.CharField(max_length=50)
    branch = models.CharField(max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)





