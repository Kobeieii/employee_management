from django.utils import timezone
from rest_framework import serializers

from employee.models.employee import Employee
from employee.models.status import Status
from employee.serializers.status import StatusSerializer


class EmployeeSerializer(serializers.ModelSerializer):
    status_id = serializers.PrimaryKeyRelatedField(
        source="status", queryset=Status.objects.all(), write_only=True
    )
    status = StatusSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = "__all__"

    def delete(self):
        instance = self.instance
        instance.deleted_at = timezone.now()
        instance.save()
