from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse


def PingView(request):
    return JsonResponse({'result': True})


def index(request):
    now = timezone.now()
    context = {'now': now}
    return render(request, 'page/index.html', context)
