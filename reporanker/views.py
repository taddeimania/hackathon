from vanilla import FormView, TemplateView

from .forms import SearchForm


class IndexView(TemplateView):
    template_name = 'reporanker/index.html'

class SearchView(FormView):
    form_class = SearchForm
    template_name = 'reporanker/search.html'
