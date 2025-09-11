from rest_framework import viewsets, permissions
from .models import Client
from .serializers import ClientSerializer

class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    permission_class = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Client.objects.for_user(self.request.users)