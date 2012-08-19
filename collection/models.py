from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from card.models import Card

# Create your models here.
class Collection(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    cards = models.ManyToManyField(Card, 
            related_name='card+', through='CollectionCards')

    def owned_list(self):
        return self.collectioncards_set.filter(card_count__gt=0)

    def wish_list(self):
        return self.collectioncards_set.filter(wish_count__gt=0)

    def trade_list(self):
        return self.collectioncards_set.filter(trade_count__gt=0)

    def _mod_card(self, id, n, op, l):
        #card = Card.objects.get(id=id)
        ccard, created = CollectionCards.objects.get_or_create(
                                        collection=self, card__id=id)
        if op == 'set':
            setattr(ccard, l, n)
        else:
            v = getattr(ccard, l)
            setattr(ccard, l, max(n+v, 0))
        ccard.save()

    def add_card(self, id, n=1):
        self._mod_card(id, n, 'add', 'card_count')

    def del_card(self, id, n=1):
        self._mod_card(id, -n, 'del', 'card_count')

    def set_card(self, id, n):
        self._mod_card(id, n, 'set', 'card_count')

    def add_wish(self, id, n=1):
        self._mod_card(id, n, 'add', 'wish_count')

    def del_wish(self, id, n=1):
        self._mod_card(id, -n, 'del', 'wish_count')

    def set_wish(self, id, n):
        self._mod_card(id, n, 'set', 'wish_count')

    def add_trade(self, id, n=1):
        self._mod_card(id, n, 'add', 'trade_count')

    def del_trade(self, id, n=1):
        self._mod_card(id, -n, 'del', 'trade_count')

    def set_trade(self, id, n):
        self._mod_card(id, n, 'set', 'trade_count')

    def set_sell_price(self, id, p):
        self._mod_card(id, p, 'set', 'sell_price')
        
    def set_buy_price(self, id, p):
        self._mod_card(id, p, 'set', 'buy_price')

class CollectionCards(models.Model):
    collection = models.ForeignKey(Collection)
    card = models.ForeignKey(Card)
    card_count = models.IntegerField(default=0)
    trade_count = models.IntegerField(default=0)
    wish_count = models.IntegerField(default=0)
    sell_price = models.FloatField(default=0.0)
    buy_price = models.FloatField(default=0.0)

admin.site.register(Collection)
