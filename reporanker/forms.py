from django import forms


class SearchForm(forms.Form):
    terms = forms.CharField(max_length=100)
