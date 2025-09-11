from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.audits.models import Audit

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        ct = ContentType.objects.get_for_model(Audit)
        perms = Permission.objects.filter(content_type=ct)
        user_group, _ = Group.objects.get_or_create(name="audit_user")
        manager_group, _ = Group.objects.get_or_create(name="audit_manager")
        user_group.permissions.set(perms.filter(codename__in=["view_audit", "add_audit", "change_audit"]))
        manager_group.permissions.set(perms)
        self.stdout.write(self.style.SUCCESS("Audit roller kuruldu."))