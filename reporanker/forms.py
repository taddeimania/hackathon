from django import forms

from .models import Review


class SearchForm(forms.Form):
    terms = forms.CharField(max_length=100)


class ReviewForm(forms.ModelForm):

    def __init__(self, **kwargs):
        super(ReviewForm, self).__init__(**kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['repo'].widget = forms.HiddenInput()
        self.fields['comment'].widget.attrs['class'] = 'form-control'
        self.fields['octocats'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Review
