from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Complaint, Escalation, Notification

# SLA time limits per priority (in hours)
SLA_HOURS = {
    'critical' : 2,
    'high'     : 8,
    'medium'   : 24,
    'low'      : 48,
}

class Command(BaseCommand):
    help = 'Auto-creates escalations for complaints that have breached their SLA'

    def handle(self, *args, **kwargs):
        now = timezone.now()

        # Get all unresolved complaints
        active_complaints = Complaint.objects.filter(
            status__in=['pending', 'in_progress']
        ).select_related('user', 'category')

        escalated_count = 0

        for complaint in active_complaints:
            # Skip if already escalated
            if Escalation.objects.filter(complaint=complaint).exists():
                continue

            # Get SLA hours for this complaint's priority
            sla_hours = SLA_HOURS.get(complaint.priority_level, 24)

            # Calculate deadline from when complaint was filed
            deadline = complaint.created_at + timezone.timedelta(hours=sla_hours)

            # Check if SLA has been breached
            if now > deadline:
                # Create escalation
                Escalation.objects.create(
                    complaint    = complaint,
                    sla_deadline = deadline,
                    reason       = f'SLA of {sla_hours}h breached for {complaint.priority_level} priority complaint.'
                )

                # Notify the user
                Notification.objects.create(
                    user      = complaint.user,
                    complaint = complaint,
                    message   = f'Your complaint #{complaint.id} has been escalated due to SLA breach. Admin has been notified.'
                )

                escalated_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f'Escalated complaint #{complaint.id} ({complaint.priority_level})'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Done. {escalated_count} new escalation(s) created.'
            )
        )
