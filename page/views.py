from django.http import JsonResponse
from django.views.generic import TemplateView
from . import mastodon_func
from dotenv import load_dotenv
load_dotenv()


def PingView(request):
    return JsonResponse({'result': True})


class IndexView(TemplateView):
    template_name = "page/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        responses = mastodon_func.timelines(10)
        context['timeline'] = sorted(responses, key=lambda x: -(x.reblogs_count * 2 + x.favourites_count))
        return context
