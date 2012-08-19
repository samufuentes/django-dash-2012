from django import forms

class SearchCardForm(forms.Form):
    search_text = forms.CharField()

class CollectionForm(forms.Form):
    name = forms.CharField()

class AddCardForm(forms.Form):
    n = forms.IntegerField()

class SetPriceForm(forms.Form):
    p = forms.FloatField()
