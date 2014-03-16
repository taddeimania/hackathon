import json

import requests
from django import http
from vanilla.views import FormView, TemplateView
from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse

from .forms import SearchForm, ReviewForm
from .models import Repo, ReviewOpinion, Review


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

                repos = Repo.objects.filter(full_name=repo['full_name'])
                if repos:
                    repo_contents['octocats'] = repos[0].get_average_octocats()
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
        context['average_octocats'] = repo.get_average_octocats()
        context['object'] = repo
        context['request'] = self.request
        reviews = []
        for review in repo.ordered_review_set().all()[:10]:
            user_opinion = review.reviewopinion_set.all().filter(user=self.request.user)
            helpful = user_opinion[0].helpful if user_opinion else None
            item = {
                'review': review,
                'opinions': review.reviewopinion_set.all(),
                'user_opinion': user_opinion,
                'helpful': helpful
            }
            reviews.append(item)
        context['reviews'] = reviews
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


class RepoRepView(FormView):

    def post(self, request, *args, **kwargs):
        post_data = request.POST.dict()
        helpful = bool('up' == post_data['vote'])
        opinion = ReviewOpinion.objects.filter(
            user=self.request.user,
            review=Review.objects.get(pk=post_data['review']))
        if opinion:
            opinion.update(helpful=helpful)
        else:
            ReviewOpinion.objects.create(
                user=self.request.user,
                review=Review.objects.get(pk=post_data['review']),
                helpful=helpful,
            )
        return http.HttpResponse(content=json.dumps({'vote': helpful}), content_type="application/json")
