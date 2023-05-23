from django.http import JsonResponse
from django.views.generic import TemplateView
from . import mastodon_func, chatgpt_func


def ping_view(request):
    return JsonResponse({'result': True})


class IndexView(TemplateView):
    template_name = "page/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        timelines = self.get_timelines()
        mode = self.request.GET.get('mode')
        if mode == "sort":
            timelines = self.sort_timelines(timelines)
        elif mode == 'gpt':
            timelines, gpt_response = self.analyze_timelines_with_gpt(timelines)
            context['gpt_response'] = gpt_response
        context['timeline'] = timelines

        return context

    def get_timelines(self) -> list:
        if self.request.GET.get('page'):
            page = int(self.request.GET.get('page', 3))
            return mastodon_func.timelines_page(page)
        elif self.request.GET.get('hours'):
            hours = int(self.request.GET.get('hours'))
            return mastodon_func.timelines_hours(hours)
        else:
            return mastodon_func.timelines_last(mastodon_func.fetch_me().id)

    def sort_timelines(self, timelines: list) -> list:
        reb = int(self.request.GET.get('reb', 2))
        fav = int(self.request.GET.get('fav', 1))
        sorted_timelines = sorted(timelines, key=lambda x: -(x.reblogs_count * reb + x.favourites_count * fav))
        if self.request.GET.get('high'):
            high = int(self.request.GET.get('high'))
            return sorted_timelines[:high]
        return sorted_timelines

    def analyze_timelines_with_gpt(self, timelines: list) -> tuple[list, str]:
        reb = int(self.request.GET.get('reb', 2))
        fav = int(self.request.GET.get('fav', 1))
        high = int(self.request.GET.get('high', 50))
        sorted_timelines = sorted(timelines, key=lambda x: -(x.reblogs_count * reb + x.favourites_count * fav))
        trimmed_timelines = sorted_timelines[:high]
        id_list, gpt_response = chatgpt_func.analyze_toots(trimmed_timelines)
        gpt_timelines = [toot for toot in trimmed_timelines if toot.id in id_list]
        return gpt_timelines, gpt_response
