from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.forms.util import ErrorList


from card.models import Card
from forms import SearchCardForm

def home(request):
    return render_to_response('home.html', {}, context_instance=RequestContext(request))

def cards(request):
    cards = Card.objects.all()[:10]
    selected = 'cards'
    viewing = 'collection'
    return render_to_response('cards/index.htm', {'cards': cards, 'viewing': viewing, 'selected': selected}, context_instance=RequestContext(request))

def card_statistics(request):
    selected = 'statistics'
    viewing = 'collection'
    return render_to_response('cards/statistics.htm', {'viewing': viewing, 'selected': selected}, context_instance=RequestContext(request))

def card_detail(request, id):
    card = Card.objects.get(id=id)
    return render_to_response('cards/detail.htm', {'data': card.data}, context_instance=RequestContext(request))

def search_card(request):
    if request.method == 'POST':
        form = SearchCardForm(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['search_text']
            # Return the first 10 results (ordered) for the user to choose.
            # Error if no results are found.
            cards = Card.freesearch(search_text)[:10]
            if cards != []:
                viewing = 'search'
                return HttpResponseRedirect('/cards/index.htm', {'cards': cards, 'viewing': viewing}, context_instance=RequestContext(request))
            form._errors['search_text'] = ErrorList([u'Cannot find any card with that name'])
    else:
        form = SearchCardForm()

    return render(request, 'search.htm', {'form': form,}, context_instance=RequestContext(request))
