from rest_framework import mixins, viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from employee.models.position import Position
from employee.serializers.position import PositionSerializer


class PositionViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["name"]
    filterset_fields = {
        "name": ["exact", "icontains", "startswith", "endswith", "in"],
        "salary": ["exact", "gt", "lt", "gte", "lte"],
    }

    def get_queryset(self):
        return self.queryset.filter(deleted_at__isnull=True)
