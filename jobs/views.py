from datetime import timedelta

from django.utils import timezone

from rest_framework import (
    viewsets,
    status,
)

from rest_framework.decorators import action

from rest_framework.response import Response

from .models import (
    Job,
    Tool,
    MachineCheck,
    Workpiece,
    Operation,
)

from .serializers import (
    JobSerializer,
    ToolSerializer,
    MachineCheckSerializer,
    WorkpieceSerializer,
    OperationSerializer,
)


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class ToolViewSet(viewsets.ModelViewSet):
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer


class MachineCheckViewSet(viewsets.ModelViewSet):
    queryset = MachineCheck.objects.all()
    serializer_class = MachineCheckSerializer


class WorkpieceViewSet(viewsets.ModelViewSet):
    queryset = Workpiece.objects.all()
    serializer_class = WorkpieceSerializer


class OperationViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer

    def retrieve(self, request, *args, **kwargs):
        operation = self.get_object()

        self.update_progress(operation)

        return Response(
            OperationSerializer(operation).data
        )

    def update_progress(self, operation):
        if operation.status != "RUNNING":
            return

        if not operation.started_at:
            return

        elapsed = (
            timezone.now() -
            operation.started_at
        ).total_seconds()

        # Simulation:
        # 10 seconds = complete operation.
        progress = min(
            100,
            int(elapsed * 10)
        )

        operation.progress = progress

        quantity = operation.job.quantity

        operation.completed_parts = int(
            quantity * progress / 100
        )

        if progress >= 100:
            operation.status = "COMPLETED"
            operation.completed_parts = quantity

        operation.save(
            update_fields=[
                "status",
                "progress",
                "completed_parts",
            ]
        )

    @action(detail=True, methods=["post"])
    def start(self, request, pk=None):
        operation = self.get_object()

        self.update_progress(operation)

        if operation.status == "COMPLETED":
            return Response(
                OperationSerializer(operation).data,
                status=status.HTTP_400_BAD_REQUEST
            )

        operation.status = "RUNNING"

        if not operation.started_at:
            operation.started_at = timezone.now()

        operation.save()

        return Response(
            OperationSerializer(operation).data
        )

    @action(detail=True, methods=["post"])
    def stop(self, request, pk=None):
        operation = self.get_object()

        self.update_progress(operation)

        if operation.status == "RUNNING":
            operation.status = "STOPPED"
            operation.save(
                update_fields=["status"]
            )

        return Response(
            OperationSerializer(operation).data
        )

    @action(detail=True, methods=["post"])
    def reset(self, request, pk=None):
        operation = self.get_object()

        operation.status = "READY"
        operation.progress = 0
        operation.completed_parts = 0
        operation.started_at = None

        operation.save()

        return Response(
            OperationSerializer(operation).data
        )