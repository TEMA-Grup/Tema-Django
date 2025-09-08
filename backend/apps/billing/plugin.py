from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class PluginMeta:
    code: str
    title: str
    version: str
    dependencies: Optional[List[str]] = None
    menus: Optional[List[Dict[str, Any]]] = None

    def on_enabled(self, tenant): ...
    def on_disabled(self, tenant): ...


meta = PluginMeta(
    code="billing",
    title="Billing / Faturalama",
    version="1.0.0",
    dependencies=["companies"],
    menus=[{"path": "/billing/", "label": "Faturalar"}],
)


def on_enabled_for_tenant(tenant):
    pass
