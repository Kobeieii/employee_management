from django.utils import timezone
from rest_framework import serializers

from employee.models.department import Department
from employee.serializers.employee import EmployeeSerializer


class DepartmentSerializer(serializers.ModelSerializer):
    manager = EmployeeSerializer()
    class Meta:
        model = Department
        fields = "__all__"

    def delete(self):
        instance = self.instance
        instance.deleted_at = timezone.now()
        instance.save()
