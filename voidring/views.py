from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext


from card.models import Card
from forms import SearchCardForm

def home(request):
    return render_to_response('home.html', {}, context_instance=RequestContext(request))

def cards(request):
    cards = Card.objects.all
    selected = "cards"
    return render_to_response('cards/index.htm', {'cards': cards, 'selected': selected}, context_instance=RequestContext(request))

def card_statistics(request):
    selected = "statistics"
    return render_to_response('cards/statistics.htm', {'selected': selected})

def card_detail(request, id):
    card = Card.objects.get(id=id)
    return render_to_response('cards/detail.htm', {'data': card.data})

def search_card(request):
    if request.method == 'POST':
        form = SearchCardForm(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['search_text']
            card_id = Card.freesearch(search_text)[0].id
            return HttpResponseRedirect('/cards/'+card_id)
    else:
        form = SearchCardForm()

    return render(request, 'templates/search.html', {'form': form,})

