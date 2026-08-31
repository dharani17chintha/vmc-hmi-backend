from rest_framework.routers import DefaultRouter

from .views import (
    JobViewSet,
    ToolViewSet,
    MachineCheckViewSet,
    WorkpieceViewSet,
    OperationViewSet,
)


router = DefaultRouter()

router.register(
    r"jobs",
    JobViewSet
)

router.register(
    r"tools",
    ToolViewSet
)

router.register(
    r"machine-checks",
    MachineCheckViewSet
)

router.register(
    r"workpieces",
    WorkpieceViewSet
)

router.register(
    r"operations",
    OperationViewSet
)


urlpatterns = router.urls