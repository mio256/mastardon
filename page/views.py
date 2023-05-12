import os
from django.http import JsonResponse
from django.views.generic import TemplateView
from mastodon import Mastodon
from dotenv import load_dotenv
load_dotenv()


def PingView(request):
    return JsonResponse({'result': True})


class IndexView(TemplateView):
    template_name = "page/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mastodon = Mastodon(
            os.environ['CLIENT_ID'],
            os.environ['CLIENT_SECRET'],
            os.environ['ACCESS_TOKEN'],
            os.environ['API_BASE_URL'],
        )
        response = mastodon.timeline_home()
        context['timeline'] = response
        return context
