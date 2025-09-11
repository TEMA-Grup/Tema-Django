import importlib
from django.db import transaction
from .models import Plugin, CompanyPlugin

@transaction.atomic
def enable_plugin_for_company(plugin_code: str, company):
    plugin = Plugin.objects.get(code=plugin_code)
    cp, _ = CompanyPlugin.objects.update_or_create(
        company=company, plugin=plugin, defaults={"enabled": True}
    )
    
    try:
        mod = importlib.import_module(f"apps.{plugin_code}.plugin")
        meta = getattr(mod, "meta", None)
        if meta and hasattr(meta, "on_enabled"):
            meta.on_enabled(company)
    except ModuleNotFoundError:
        pass
    return cp

@transaction.atomic
def disable_plugin_for_company(plugin_code: str, company):
    plugin = Plugin.objects.get(code=plugin_code)
    CompanyPlugin.objects.update_or_create(
        company=company, plugin=plugin, defaults={"enabled": False}
    )
    try:
        mod = importlib.import_module(f"apps.{plugin_code}.plugin")
        meta = getattr(mod, "meta", None)
        if meta and hasattr(meta, "on_disabled"):
            meta.on_disabled(company)
    except ModuleNotFoundError:
        pass