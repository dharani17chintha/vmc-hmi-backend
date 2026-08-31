from django.db import models


class Job(models.Model):
    job_number = models.CharField(
        max_length=50,
        unique=True
    )

    quantity = models.PositiveIntegerField()

    material = models.CharField(
        max_length=100
    )

    fixture = models.CharField(
        max_length=100
    )

    work_offset = models.CharField(
        max_length=20
    )

    drawing_number = models.CharField(
        max_length=50
    )

    drawing_revision = models.CharField(
        max_length=10
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.job_number


class Tool(models.Model):
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="tools"
    )

    tool_number = models.CharField(
        max_length=20
    )

    tool_type = models.CharField(
        max_length=100
    )

    purpose = models.CharField(
        max_length=100
    )

    confirmed = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.tool_number} - {self.tool_type}"


class MachineCheck(models.Model):
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="machine_checks"
    )

    name = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    completed = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.name


class Workpiece(models.Model):
    job = models.OneToOneField(
        Job,
        on_delete=models.CASCADE,
        related_name="workpiece"
    )

    orientation = models.TextField()

    orientation_confirmed = models.BooleanField(
        default=False
    )

    datum = models.CharField(
        max_length=100
    )

    datum_confirmed = models.BooleanField(
        default=False
    )

    clamping = models.TextField()

    clamping_confirmed = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"Workpiece - {self.job.job_number}"


class Operation(models.Model):

    STATUS_CHOICES = [
        ("READY", "Ready"),
        ("RUNNING", "Running"),
        ("STOPPED", "Stopped"),
        ("COMPLETED", "Completed"),
    ]

    job = models.OneToOneField(
        Job,
        on_delete=models.CASCADE,
        related_name="operation"
    )

    name = models.CharField(
        max_length=100
    )

    program = models.CharField(
        max_length=50
    )

    revision = models.CharField(
        max_length=10
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="READY"
    )

    progress = models.PositiveIntegerField(
        default=0
    )

    completed_parts = models.PositiveIntegerField(
        default=0
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.name} - {self.job.job_number}"