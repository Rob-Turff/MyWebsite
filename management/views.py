from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from management.models import Management


@login_required
def display_ip(request):
    management_obj = Management.objects.first()
    if request.method == "POST":
        ip = request.POST.get("ip")
        if Management.objects.count() == 1:
            management_obj.ip = ip
        else:
            management_obj = Management(ip=ip)
        management_obj.save()
        return HttpResponse("ip read " + str(ip))
    else:
        if Management.objects.count() == 1:
            return HttpResponse(management_obj.ip)
        else:
            return HttpResponse("No stored ip address")
