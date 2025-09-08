from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Client

@login_required
def client_list(request):
    qs = Client.objects.for_user(request.user)
    return render(request, "clients/list.html", {"clients": qs})

def clients_home(request):
    return HttpResponse("Clients app çalışıyor")