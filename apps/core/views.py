from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.core.models import Plugin, CompanyPlugin

@login_required
def home(request):
    company = getattr(request, "tenant", None)
    plugins = Plugin.objects.all().order_by("code")
    
    states = {}
    for p in plugins:
        if p.is_core or p.enabled_globally:
            states[p.code] = True
        elif company:
            states[p.code] = CompanyPlugin.objects.filter(
                company=company, plugin=p, enabled=True
            ).exists()
        else:
            states[p.code] = False
    
    ctx = {
        "company": company,
        "plugins": plugins,
        "states": states,
    }
    return render(request, "core/home.html", ctx)