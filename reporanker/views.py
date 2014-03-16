import json

import requests
from vanilla.views import FormView, TemplateView
from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.db.models import Avg

from .forms import SearchForm, ReviewForm
from .models import Repo


class IndexView(TemplateView):
    template_name = 'reporanker/index.html'


class SearchView(LoginRequiredMixin, FormView):
    form_class = SearchForm
    template_name = 'reporanker/search.html'

    def get_average_octocats_for_repo(self, full_name):
        repo = Repo.objects.filter(full_name=full_name)
        if repo:
            review_average = repo[0].review_set.all().aggregate(Avg('octocats'))['octocats__avg']
            if review_average:
                return int(round(review_average))

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
                repo_contents['octocats'] = self.get_average_octocats_for_repo(repo['full_name'])
                repo_contents['full_name'] = repo['full_name']
                repo_contents['name'] = repo['name']
                repo_contents['owner'] = repo['owner']['login']
                repo_contents['forks'] = repo['forks']
                repo_contents['stars'] = repo['stargazers_count']
                repo_contents['issues'] = repo['open_issues_count']
                context['repos'].append(repo_contents)
        return context


class RepoDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'reporanker/repo_detail.html'

    def get_context_data(self, form=None):
        context = super(RepoDetailView, self).get_context_data(form=form)
        full_name = self.kwargs['slug']

        try:
            repo = Repo.objects.get(
                full_name=full_name
            )
        except:
            url = 'https://api.github.com/repos/{0}'.format(full_name)
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

        context['user_reviewed'] = repo.review_set.filter(user=self.request.user).exists()
        context['object'] = repo
        return context


class RepoReviewView(FormView):
    form_class = ReviewForm
    template_name = "reporanker/repo_review.html"
    success_url = ""

    def post(self, *args, **kwargs):
        kwargs.pop('pk')
        return super(RepoReviewView, self).post(*args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super(RepoReviewView, self).form_valid(form)

    def get_success_url(self):
        repo = Repo.objects.get(pk=self.kwargs.get('pk'))
        return reverse("repo-detail-view", kwargs={'slug': repo.full_name})

    def get_form(self, data=None, files=None, **kwargs):
        user = self.request.user
        repo = Repo.objects.get(pk=self.kwargs.get('pk'))
        kwargs['initial'] = {'user': user, 'repo': repo}
        form = super(RepoReviewView, self).get_form(data=data, files=files, **kwargs)
        return form
