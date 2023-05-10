from django.http import JsonResponse


def PingView(request):
    return JsonResponse({'result': True})
