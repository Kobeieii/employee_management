from django.db import models


class StatusChoices(models.TextChoices):
    RECRUITMENT = "Recruitment"
    ONBOARDING = "Onboarding"
    PROBATION = "Probation"
    NORMAL = "Normal"
    RESIGNED = "Resigned"
    SUSPENDED = "Suspended"
    TERMINATED = "Terminated"
    RETIRED = "Retired"
    CONTRACT = "Contract"


class Status(models.Model):

    name = models.CharField(max_length=20, choices=StatusChoices.choices, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_default_status():
        status, _ = Status.objects.get_or_create(name=StatusChoices.NORMAL)
        return status.id
