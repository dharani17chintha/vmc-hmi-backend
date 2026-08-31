from rest_framework import serializers

from .models import (
    Job,
    Tool,
    MachineCheck,
    Workpiece,
    Operation,
)


class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = "__all__"


class MachineCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineCheck
        fields = "__all__"


class WorkpieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workpiece
        fields = "__all__"


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = "__all__"


class JobSerializer(serializers.ModelSerializer):
    operation = OperationSerializer(read_only=True)
    tools = ToolSerializer(
        many=True,
        read_only=True
    )
    machine_checks = MachineCheckSerializer(
        many=True,
        read_only=True
    )
    workpiece = WorkpieceSerializer(
        read_only=True
    )

    class Meta:
        model = Job
        fields = [
            "id",
            "job_number",
            "quantity",
            "material",
            "fixture",
            "work_offset",
            "drawing_number",
            "drawing_revision",
            "created_at",
            "updated_at",
            "operation",
            "tools",
            "machine_checks",
            "workpiece",
        ]