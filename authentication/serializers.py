# accounts/serializers.py
from rest_framework import serializers
from authentication.models import User
from employee.models import Employee  # import your employee model


class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    address = serializers.CharField()
    is_manager = serializers.BooleanField()
    status_id = serializers.IntegerField()
    position_id = serializers.IntegerField()
    image = serializers.ImageField(required=False)

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "address",
            "is_manager",
            "image",
        ]

    def create(self, validated_data):
        employee_data = {
            "first_name": validated_data.pop("first_name"),
            "last_name": validated_data.pop("last_name"),
            "address": validated_data.pop("address"),
            "is_manager": validated_data.pop("is_manager"),
            "image": validated_data.pop("image", None),
        }

        employee = Employee.objects.create(**employee_data)

        user = User.objects.create_user(**validated_data)
        user.employee = employee
        user.save()

        return user
