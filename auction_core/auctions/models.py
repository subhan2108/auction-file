from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

#first day start
class CustomUser(AbstractUser):
    # Add custom fields here if needed
    is_seller = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username