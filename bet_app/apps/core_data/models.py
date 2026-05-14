from django.db import models

# Create your models here.


class Countries(models.Model):

    code = models.CharField(max_length=3, unique=True, null=False)
    name = models.CharField(max_length=100, unique=True, null=False)
