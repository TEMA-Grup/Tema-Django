from django.core.management.base import BaseCommand
from django.utils.timezone import now
from apps.audits.models import Action

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        today = now().date()
        overdue = Action.objects.filter(state__in=["open", "progress"], deadline__lt=today)
        for a in overdue:
            self.stdout.write(f"Geciken aksiyon: {a.id} ({a.finding.audit.reference})")