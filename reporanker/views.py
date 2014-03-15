from vanilla import FormView

from .forms import SearchForm


class SearchView(FormView):
    form_class = SearchForm
    template_name = 'reporanker/search.html'
