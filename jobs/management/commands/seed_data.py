from django.core.management.base import BaseCommand

from jobs.models import (
    Job,
    Tool,
    MachineCheck,
    Workpiece,
    Operation,
)


class Command(BaseCommand):
    help = "Create sample VMC HMI data"

    def handle(self, *args, **options):

        # Remove existing sample job
        Job.objects.filter(
            job_number="JOB-1001"
        ).delete()

        # Create Job
        job = Job.objects.create(
            job_number="JOB-1001",
            quantity=10,
            material="Aluminum 6061",
            fixture="Machine Vice",
            work_offset="G54",
            drawing_number="DWG-1001",
            drawing_revision="A",
        )

        # Create Tools
        Tool.objects.create(
            job=job,
            tool_number="T01",
            tool_type="Ø50 Face Mill",
            purpose="Facing",
        )

        Tool.objects.create(
            job=job,
            tool_number="T02",
            tool_type="Ø10 End Mill",
            purpose="Pocket Milling",
        )

        Tool.objects.create(
            job=job,
            tool_number="T03",
            tool_type="Ø6 End Mill",
            purpose="Finishing",
        )

        # Create Machine Checks
        checks = [
            (
                "Machine Power",
                "Machine power and control system checked.",
            ),
            (
                "Emergency Stop",
                "Emergency stop circuit checked.",
            ),
            (
                "Lubrication",
                "Lubrication system checked.",
            ),
            (
                "Coolant",
                "Coolant level checked.",
            ),
            (
                "Air Pressure",
                "Required air pressure checked.",
            ),
            (
                "Machine Area",
                "Machine area cleared and safe.",
            ),
        ]

        for name, description in checks:
            MachineCheck.objects.create(
                job=job,
                name=name,
                description=description,
                completed=False,
            )

        # Create Workpiece
        Workpiece.objects.create(
            job=job,
            orientation="Datum A facing operator",
            datum="G54",
            clamping="Fully seated and securely clamped",
        )

        # Create Operation
        Operation.objects.create(
            job=job,
            name="Face & Pocket",
            program="O1001",
            revision="A",
            status="READY",
            progress=0,
            completed_parts=0,
        )

        self.stdout.write(
            self.style.SUCCESS(
                "VMC sample data created successfully."
            )
        )