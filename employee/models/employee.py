from django.utils import timezone
from django.db import models
from employee.models.status import Status


class Employee(models.Model):
    first_name = models.CharField(max_length=125)
    last_name = models.CharField(max_length=125)
    address = models.TextField()
    is_manager = models.BooleanField(default=False)
    status = models.ForeignKey(
        Status, on_delete=models.CASCADE, default=Status.get_default_status
    )
    image = models.ImageField(upload_to="employee_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        unique_together = ("first_name", "last_name")

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()
