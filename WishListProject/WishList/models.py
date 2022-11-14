from random import randint

from django.db import models
from django.db.models import Count


class Object(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)

class Person(models.Model):
    def random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]
    name = models.CharField(max_length=20)
    all_ids = models.JSONField(default=list)
