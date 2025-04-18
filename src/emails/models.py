from django.db import models

# Create your models here.
class Email(models.Model):
    email = models.EmailField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    

class EmailVerification(models.Model):
    email = models.EmailField()
    # token
    timestamp = models.DateTimeField(auto_now_add=True)