from django.utils import timezone
from django.db import models
from employee.models.employee import Employee


class Department(models.Model):
    name = models.CharField(max_length=125, unique=True)
    manager = models.OneToOneField(Employee, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()
