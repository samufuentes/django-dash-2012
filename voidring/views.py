from django.shortcuts import render_to_response
from django.template import RequestContext
from card.models import Card

def home(request):
    return render_to_response('home.html', {}, context_instance=RequestContext(request))

def cards(request):
    cards = Card.objects.all
    selected = "cards"
    return render_to_response('cards/index.htm', {'cards': cards, 'selected': selected}, context_instance=RequestContext(request))

def card_statistics(request):
    selected = "statistics"
    return render_to_response('cards/statistics.htm', {'selected': selected}, context_instance=RequestContext(request))

def card_detail(request, id):
    card = Card.objects.get(id=id)
    return render_to_response('cards/detail.htm', {'data': card.data}, context_instance=RequestContext(request))
