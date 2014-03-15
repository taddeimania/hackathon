import json

import requests
from vanilla.views import FormView, TemplateView, TemplateView
from braces.views import LoginRequiredMixin

from .forms import SearchForm
from .models import Repo


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
            context['repos'] = []
            for repo in response['items']:
                repo_contents = {}
                repo_contents['full_name'] = repo['full_name']
                repo_contents['name'] = repo['name']
                repo_contents['owner'] = repo['owner']['login']
                repo_contents['forks'] = repo['forks']
                repo_contents['stars'] = repo['stargazers_count']
                repo_contents['issues'] = repo['open_issues_count']
                context['repos'].append(repo_contents)
        return context


class RepoDetailView(TemplateView):
    template_name = 'reporanker/repo_detail.html'

    def get_context_data(self):
        context = super(RepoDetailView, self).get_context_data()

        owner, repo = self.kwargs['owner'], self.kwargs['repo']

        try:
            repo = Repo.objects.get(
                full_name="{}/{}".format(self.kwargs['owner'], self.kwargs['repo'])
            )
        except:
            #TODO: fire api request
            url = 'https://api.github.com/repos/{0}/{1}'.format(owner, repo)
            print url
            result = requests.get(url)
            response_json = result.text
            response = json.loads(response_json)

            repo = Repo.objects.create(
                name=response['name'],
                full_name=response['full_name'],
                owner_id=response['owner']['id'],
                owner_name=response['owner']['login'],
                owner_gravatar_url=response['owner']['avatar_url'],
                owner_url=response['owner']['url'],
                html_url=response['html_url'],
                description=response['description'],
                url=response['url'],
                star_count=response['stargazers_count'],
                watchers_count=response['watchers_count'],
                forks_count=response['forks_count'],
                language=response['language'],
                open_issue_count=response['open_issues_count']
            )

        context['object'] = repo

        return context
