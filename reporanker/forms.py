from django import forms

from .models import Review


class SearchForm(forms.Form):
    terms = forms.CharField(max_length=100)


class ReviewForm(forms.ModelForm):

    def __init__(self, **kwargs):
        super(ReviewForm, self).__init__(**kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['repo'].widget = forms.HiddenInput()

    class Meta:
        model = Review
