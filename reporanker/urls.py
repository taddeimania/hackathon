from django.conf.urls import patterns, url

from .views import SearchView


urlpatterns = patterns(
    '',
    url(r'^search/$', SearchView.as_view(), name='search-view'),
)
