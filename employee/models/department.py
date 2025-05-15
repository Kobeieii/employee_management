from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=125, unique=True)
    manager = models.OneToOneField("Employee", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
