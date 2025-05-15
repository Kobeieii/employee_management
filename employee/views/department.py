from rest_framework import mixins, viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from employee.models.department import Department
from employee.serializers.department import DepartmentSerializer


class DepartmentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["name"]
    filterset_fields = {
        "name": ["exact", "icontains", "startswith", "endswith", "in"],
        "manager__first_name": ["exact", "icontains", "startswith", "endswith", "in"],
        "manager__last_name": ["exact", "icontains", "startswith", "endswith", "in"],
    }

    def get_queryset(self):
        return self.queryset.filter(deleted_at__isnull=True)

    def perform_destroy(self, instance):
        serializer = self.get_serializer(instance)
        serializer.delete()
