from django.utils import timezone
from rest_framework import serializers

from employee.models.position import Position


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = "__all__"

    def delete(self):
        instance = self.instance
        instance.deleted_at = timezone.now()
        instance.save()
