from . import mastodon_func, chatgpt_func
from django.http import JsonResponse
from django.views.generic import TemplateView


def PingView(request):
    return JsonResponse({'result': True})


class IndexView(TemplateView):
    template_name = "page/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.GET.get('hours'):
            hours = int(self.request.GET.get('hours'))
            mastodon_timelines = mastodon_func.timelines_hours(hours)
        else:
            page = int(self.request.GET.get('page', 3))
            mastodon_timelines = mastodon_func.timelines_page(page)

        mode = self.request.GET.get('mode')

        if mode == 'gpt':
            if self.request.GET.get('high'):
                high = int(self.request.GET.get('high', 20))
                reb = int(self.request.GET.get('reb', 2))
                fav = int(self.request.GET.get('fav', 1))
                mastodon_timelines = sorted(mastodon_timelines, key=lambda x: -(x.reblogs_count * reb + x.favourites_count * fav))
                mastodon_timelines = mastodon_timelines[:high]
            id_list, gpt_response = chatgpt_func.analyze_toot(mastodon_timelines)
            timeline = []
            for i in range(len(mastodon_timelines)):
                for id in id_list:
                    if id == mastodon_timelines[i].id:
                        timeline.append(mastodon_timelines[i])
            context['gpt_response'] = gpt_response
            context['timeline'] = timeline
        elif mode == 'sort':
            reb = int(self.request.GET.get('reb', 2))
            fav = int(self.request.GET.get('fav', 1))
            mastodon_timelines = sorted(mastodon_timelines, key=lambda x: -(x.reblogs_count * reb + x.favourites_count * fav))
            if self.request.GET.get('high'):
                high = int(self.request.GET.get('high', 20))
                mastodon_timelines = mastodon_timelines[:high]
            context['timeline'] = mastodon_timelines
        else:
            context['timeline'] = mastodon_timelines

        return context
