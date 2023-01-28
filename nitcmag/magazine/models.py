from django.db import models
from django.core.validators import MinLengthValidator

# Create your modelsc here.

# FIX FORIEGN KEYS...

class Login_cred(models.Model):
    U_Id = models.CharField(primary_key=True, max_length=9, validators=[MinLengthValidator(9)])
    Password = models.CharField(max_length=30)
    R_Id = models.IntegerField()

class Reviewer(models.Model):
    Reviewer_Id = models.CharField(primary_key=True, max_length=9, validators=[MinLengthValidator(9)])
    Name = models.CharField(max_length=40)
    
class Article(models.Model):
    Article_Id = models.IntegerField(primary_key=True)
    Title = models.CharField(max_length = 100)
    Author = models.CharField(max_length = 40)
    Content = models.CharField(max_length = 2000)
    Reviewer = models.ForeignKey(Reviewer,to_field="Reviewer_Id", on_delete=models.CASCADE)
    Status = models.IntegerField()
    Rating = models.IntegerField(default=None)

