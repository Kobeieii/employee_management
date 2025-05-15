from rest_framework import viewsets, mixins
from authentication.serializers import RegisterSerializer


class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = RegisterSerializer
    queryset = None
