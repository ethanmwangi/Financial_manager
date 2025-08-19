from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Extra fields we might use later
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    financial_goal = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username
