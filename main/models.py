from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    passowrd = models.CharField(max_length=45)
    username = models.CharField(max_length=45)
    date_of_birth = models.DateField()

