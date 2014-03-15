from django.conf.urls import patterns, url

from .views import SearchView, IndexView


urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='landing-page'),
    url(r'^search/$', SearchView.as_view(), name='search-view'),
)
