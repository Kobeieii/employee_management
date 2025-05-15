from django.utils import timezone
from rest_framework import serializers

from employee.models.status import Status


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"

    def delete(self):
        instance = self.instance
        instance.deleted_at = timezone.now()
        instance.save()
