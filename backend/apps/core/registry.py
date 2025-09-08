import importlib
from django.apps import apps as django_apps
from .models import Plugin

class PluginRegistry:
    _cache = {}
    
    @classmethod
    def discover(cls):
        cls._cache.clear()
        for appcfg in django_apps.get_app_configs():
            try:
                mod = importlib.import_module(f"{appcfg.name}.plugin")
            except ModuleNotFoundError:
                continue
            meta = getattr(mod, "meta", None)
            if meta and getattr(meta, "code", None):
                cls._cache[meta.code] = meta
            
    @classmethod
    def sync_db(cls):
        for code, meta in cls._cache.items():
            Plugin.objects.update_or_create(
                code=code,
                defaults={"title": meta.title, "version": meta.version},
            )
            
    @classmethod
    def get(cls, code):
        return cls._cache.get(code)
    
    @classmethod
    def all_codes(cls):
        return list(cls._cache.keys())