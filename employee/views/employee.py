from rest_framework import mixins, viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from employee.models.employee import Employee
from employee.serializers.employee import EmployeeSerializer


class EmployeeViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["first_name", "last_name"]
    filterset_fields = {
        "first_name": ["exact", "icontains", "startswith", "endswith", "in"],
        "last_name": ["exact", "icontains", "startswith", "endswith", "in"],
        "status__name": ["exact", "icontains", "startswith", "endswith", "in"],
    }

    def get_queryset(self):
        return self.queryset.filter(deleted_at__isnull=True)
