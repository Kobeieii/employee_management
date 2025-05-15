from rest_framework import serializers
from authentication.models import User
from employee.models.employee import Employee


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    address = serializers.CharField()
    image = serializers.ImageField(required=False)

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        employee_data = {
            "first_name": validated_data.pop("first_name"),
            "last_name": validated_data.pop("last_name"),
            "address": validated_data.pop("address"),
            "image": validated_data.pop("image", None),
        }

        employee = Employee.objects.create(**employee_data)
        user = User.objects.create_user(**validated_data)
        user.employee = employee
        user.save()

        return user
    
    def to_representation(self, instance):
        return {
            "email": instance.email,
            "employee": {
                "first_name": instance.employee.first_name,
                "last_name": instance.employee.last_name,
                "address": instance.employee.address,
            }
        }
