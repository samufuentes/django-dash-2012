from django import forms

class SearchCardForm(forms.Form):
    searchtext = forms.CharField()
