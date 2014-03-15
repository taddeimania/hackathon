import json

import requests
from vanilla.views import FormView, TemplateView
from braces.views import LoginRequiredMixin

from .forms import SearchForm


class IndexView(TemplateView):
    template_name = 'reporanker/index.html'


class SearchView(LoginRequiredMixin, FormView):
    form_class = SearchForm
    template_name = 'reporanker/search.html'

    def get_context_data(self, form=None):
        context = super(SearchView, self).get_context_data(form=form)
        terms = self.request.GET.get('terms', None)
        if terms:
            git_hub_search_url = 'https://api.github.com/search/repositories?q={}'.format(terms)
            response_json = requests.get(git_hub_search_url).text
            response = json.loads(response_json)
            context['urls'] = []
            for repo in response['items']:
                context['urls'].append(repo['url'])
        return context
