from django.shortcuts import render_to_response
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.forms.util import ErrorList
from django.contrib.auth.decorators import login_required


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
                return render_to_response('cards/index.htm', {'cards': cards, 'viewing': viewing}, context_instance=RequestContext(request))
            form._errors['search_text'] = ErrorList([u'Cannot find any card with that name'])
    else:
        form = SearchCardForm()

    return render(request, 'search.htm', {'form': form,}, context_instance=RequestContext(request))

@login_required
def create_collection(request):
    if request.method == 'POST':
        form = CollectionForm(request.POST)
        if form.isvalid():
            name = form.cleaned_data['search_text']
            collection, created = Collection.objects.get_or_create(
                            user__id=request.user_id, name=name)
            selected = 'cards'
            viewing = 'collection'
            if created:
                collection.save()
            for card in collection.card_list():
                card.card.n = card.card_count()
            cards = [c.card for c in collection.card_list()]
            return render_to_response('cards/index.htm', {'cards': cards, 'viewing': viewing, 'selected': selected}, context_instance=RequestContext(request))
    else:
        form = CollectionForm()
    return render(request, 'collection.htm', {'form': form}, context_instance=RequestContext(request))

@login_required
def add_card(request, collection, card):
    if request.method == 'POST':
        form = AddCardForm(request.POST)
        if form.isvalid():
            n = form.cleaned_data['n']
            collection = Collection.objects.get(id=collection)
            collection.add_card(card, n)
    else:
        form = CollectionForm()

