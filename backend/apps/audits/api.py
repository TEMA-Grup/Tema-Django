from rest_framework import viewsets, permissions
from .models import Audit
from .serializers import AuditSerializer

class AuditeViewSet(viewsets.ModelViewSet):
    serializer_class = AuditSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(name__icontains=q) | qs.filter(reference__icontains=q)
        return qs