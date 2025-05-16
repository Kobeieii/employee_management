from django.utils import timezone
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=125, unique=True)
    salary = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    def delete(self):
        self.deleted_at = timezone.now()
        self.save()
