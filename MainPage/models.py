from django.db import models

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')

class Result(models.Model):
    tags = models.TextField(null=True)
