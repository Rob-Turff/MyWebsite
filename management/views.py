from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from management.models import StaticIp


class DisplayIP(APIView):
    permission_classes = [HasAPIKey | IsAuthenticated]

    @csrf_exempt
    def get(self, request):
        title = request.GET.get("title")
        try:
            static_ip = StaticIp.objects.get(title=title)
            return HttpResponse(static_ip.ip)
        except ObjectDoesNotExist:
            return HttpResponse("No stored ip address")

    @csrf_exempt
    def post(self, request):
        title = request.data.get("title")
        if title is None:
            return HttpResponse("title not set")
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        try:
            static_ip = StaticIp.objects.get(title=title)
            static_ip.ip = ip
            static_ip.save()
        except ObjectDoesNotExist:
            static_ip = StaticIp(title=title, ip=ip)
            static_ip.save()
        return HttpResponse(title + ":" + str(ip))
