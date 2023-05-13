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
            timelines = mastodon_func.timelines_hours(hours)
        else:
            page = int(self.request.GET.get('page', 3))
            timelines = mastodon_func.timelines_page(page)

        mode = self.request.GET.get('mode')
        if mode == "sort":
            reb = int(self.request.GET.get('reb', 2))
            fav = int(self.request.GET.get('fav', 1))
            timelines = sorted(timelines, key=lambda x: -(x.reblogs_count * reb + x.favourites_count * fav))
            if self.request.GET.get('high'):
                high = int(self.request.GET.get('high'))
                timelines = timelines[:high]
            context['timeline'] = timelines
        elif mode == 'gpt':
            if self.request.GET.get('high'):
                reb = int(self.request.GET.get('reb', 2))
                fav = int(self.request.GET.get('fav', 1))
                high = int(self.request.GET.get('high'))
                timelines = sorted(timelines, key=lambda x: -(x.reblogs_count * reb + x.favourites_count * fav))
                timelines = timelines[:high]
            id_list, gpt_response = chatgpt_func.analyze_toot(timelines)
            gpt_timelines = []
            for toot in timelines:
                if toot.id in id_list:
                    gpt_timelines.append(toot)
            context['gpt_response'] = gpt_response
            context['timeline'] = gpt_timelines
        else:
            context['timeline'] = timelines

        return context
