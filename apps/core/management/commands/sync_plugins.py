from django.core.management.base import BaseCommand
from apps.core.registry import PluginRegistry

class Command(BaseCommand):
    help = "Keşfedilen plugin meta bilgilerini Plugin tablosu ile senkronlar."
    
    def handle(self, *args, **kwargs):
        PluginRegistry.discover()
        PluginRegistry.sync_db()
        self.stdout.write(self.style.SUCCESS("Plugins synced."))