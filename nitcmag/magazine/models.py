from django.db import models
from django.core.validators import MinLengthValidator

# Create your modelsc here.

class Login_cred(models.Model):
    U_Id = models.CharField(primary_key=True, max_length=9, validators=[MinLengthValidator(9)])
    Password = models.CharField(max_length=30)
    R_Id = models.IntegerField()

class Reviewer(models.Model):
    Reviewer_Id = models.CharField(primary_key=True, max_length=9, validators=[MinLengthValidator(9)])
    Name = models.CharField(max_length=40)
    


