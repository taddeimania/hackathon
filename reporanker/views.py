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
            context['results'] = ['one', 'two', 'three']
        return context
