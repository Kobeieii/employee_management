from django.utils import timezone
from rest_framework import serializers

from employee.models.employee import Employee
from employee.serializers.status import StatusSerializer


class EmployeeSerializer(serializers.ModelSerializer):
    status = StatusSerializer()

    class Meta:
        model = Employee
        fields = "__all__"

    def delete(self):
        instance = self.instance
        instance.deleted_at = timezone.now()
        instance.save()
