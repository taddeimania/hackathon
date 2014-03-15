from django.conf.urls import patterns, url

from .views import SearchView, IndexView, RepoDetailView


urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='landing-page'),
    url(r'^search/$', SearchView.as_view(), name='search-view'),
    url(r'^repo/(?P<slug>.*)/$', RepoDetailView.as_view(), name='repo-detail-view'),
)
