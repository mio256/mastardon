import re
from . import mastodon_func, chatgpt_func
from django.http import JsonResponse
from django.views.generic import TemplateView


def PingView(request):
    return JsonResponse({'result': True})


class IndexView(TemplateView):
    template_name = "page/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page = int(self.request.GET.get('page', 5))
        reb = int(self.request.GET.get('reb', 2))
        fav = int(self.request.GET.get('fav', 1))
        en = bool(self.request.GET.get('en', False))
        gpt = bool(self.request.GET.get('gpt', False))

        mastodon_timelines = mastodon_func.timelines(page)

        if gpt:
            id_list = chatgpt_func.analyze_toot(mastodon_timelines)

            timeline = []
            for i in id_list:
                for j in range(20*page):
                    if i == mastodon_timelines[j].id:
                        timeline.append(mastodon_timelines[j])
            context['timeline'] = timeline
        elif en:
            context['timeline'] = sorted(mastodon_timelines,
                                         key=lambda x: -(x.reblogs_count * reb + x.favourites_count * fav + len(re.findall('[a-z]+', x.content))))
        else:
            context['timeline'] = sorted(mastodon_timelines,
                                         key=lambda x: -(x.reblogs_count * reb + x.favourites_count * fav))

        return context
