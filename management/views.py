from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from management.models import StaticIp


@login_required
def display_ip(request):
    if request.method == "POST":
        title = request.POST.get("title")
        ip = request.META.get("REMOTE_ADDR")
        try:
            static_ip = StaticIp.objects.get(title=title)
            static_ip.ip = ip
            static_ip.save()
        except ObjectDoesNotExist:
            static_ip = StaticIp(title=title, ip=ip)
            static_ip.save()
        return HttpResponse(title + ":" + str(ip))
    elif request.method == "GET":
        title = request.GET.get("title")
        try:
            static_ip = StaticIp.objects.get(title=title)
            return HttpResponse(static_ip.ip)
        except ObjectDoesNotExist:
            return HttpResponse("No stored ip address")