from functools import wraps
from django.http import Http404
from .models import Plugin, CompanyPlugin

def _is_enabled(request, plugin_code: str) -> bool:
    company = getattr(request, "tenant", None)
    try:
        plugin = Plugin.objects.get(code=plugin_code)
    except Plugin.DoesNotExist:
        return False

    if plugin.is_core or plugin.enabled_globally:
        return True
    
    if not company:
        return False
    
    return CompanyPlugin.objects.filter(company=company, plugin=plugin, enabled = True).exists()

def require_plugin(plugin_code: str):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not _is_enabled(request, plugin_code):
                raise Http404()
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator