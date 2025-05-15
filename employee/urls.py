from django.urls import path, include
from rest_framework import routers
from employee import views

router = routers.DefaultRouter()
router.register(r"department", views.DepartmentViewSet, basename="department")
router.register(r"employee", views.EmployeeViewSet, basename="employee")
router.register(r"position", views.PositionViewSet, basename="position")
router.register(r"status", views.StatusViewSet, basename="status")

urlpatterns = [
    path("", include(router.urls)),
]