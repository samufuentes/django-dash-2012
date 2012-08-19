from django import forms

class SearchCardForm(forms.Form):
    search_text = forms.CharField()
