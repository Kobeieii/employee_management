from rest_framework import serializers

from employee.models.department import Department
from employee.models.employee import Employee
from employee.serializers.employee import EmployeeSerializer


class DepartmentSerializer(serializers.ModelSerializer):
    manager_id = serializers.PrimaryKeyRelatedField(
        source="manager", queryset=Employee.objects.all(), write_only=True
    )
    manager = EmployeeSerializer(read_only=True)

    class Meta:
        model = Department
        fields = "__all__"

    def validate(self, attrs):
        manager = attrs.get("manager")
        if manager and not manager.is_manager:
            raise serializers.ValidationError(
                "This employee is not marked as a manager."
            )
        if manager and manager.deleted_at:
            raise serializers.ValidationError("This employee is deleted.")
        return super().validate(attrs)
