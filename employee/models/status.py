from django.db import models


# Status model: Contains the current status of the employee (e.g., in recruitment process, waiting for onboarding, in probation period, normal, and resigned).
class Status(models.Model):

    class StatusChoices(models.TextChoices):
        RECRUITMENT = "Recruitment"
        ONBOARDING = "Onboarding"
        PROBATION = "Probation"
        NORMAL = "Normal"
        RESIGNED = "Resigned"

    name = models.CharField(max_length=20, choices=StatusChoices.choices, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
