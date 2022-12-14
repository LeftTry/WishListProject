from random import randint

from django.db import models
from django.db.models import Count


class Object(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)

class Person(models.Model):
    name = models.CharField(max_length=20)
    all_ids = models.JSONField(default=list)
