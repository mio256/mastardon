import re
import pprint
from . import mastodon_func, chatgpt_func
from django.http import JsonResponse
from django.views.generic import TemplateView


def PingView(request):
    return JsonResponse({'result': True})


class IndexView(TemplateView):
    template_name = "page/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page = int(self.request.GET.get('page', 3))
        mode = self.request.GET.get('mode', None)
        reb = int(self.request.GET.get('reb', 2))
        fav = int(self.request.GET.get('fav', 1))

        mastodon_timelines = mastodon_func.timelines(page)

        if mode == 'gpt':
            id_list, gpt_response = chatgpt_func.analyze_toot(mastodon_timelines)

            timeline = []
            for i in range(len(mastodon_timelines)):
                for id in id_list:
                    if id == mastodon_timelines[i].id:
                        timeline.append(mastodon_timelines[i])
            context['gpt_response'] = gpt_response
            context['timeline'] = timeline
        elif mode == 'en':
            context['timeline'] = sorted(mastodon_timelines, key=lambda x: -(x.reblogs_count * reb + x.favourites_count * fav + len(re.findall('[a-z]+', x.content))))
        elif mode == 'sort':
            context['timeline'] = sorted(mastodon_timelines, key=lambda x: -(x.reblogs_count * reb + x.favourites_count * fav))
        else:
            context['timeline'] = mastodon_timelines

        return context
