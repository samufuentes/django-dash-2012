from django.db import models
from django_hstore import hstore
from django.contrib import admin
from datetime import datetime, timedelta

UPDATE_TIMES = {
    'prices': timedelta(seconds=1),
    #'prices': timedelta(hours=1),
    'data': timedelta(minutes=1),
    #'data': timedelta(days=1),
    }

class Card(models.Model):
    data = hstore.DictionaryField()
    last_data_update = models.DateTimeField()
    prices = hstore.DictionaryField()
    last_prices_update = models.DateTimeField()

    objects = hstore.HStoreManager()

    def __unicode__(self):
        card = "Card %s (updated %s)" % (str(self.data), 
                    self.last_data_update)
        prices = "Prices %s (updated %s)" % (str(self.prices), 
                    self.last_prices_update)
        return "%s\n%s" % (card, prices)

    def save(self):
        if 'data' in self._modified_attrs:
            self.last_data_update = datetime.now()
        if 'prices' in self._modified_attrs:
            self.last_prices_update = datetime.now()
        super(Card, self).save()

    def __init__(self, *args, **kwargs):
        super(Card, self).__init__(*args, **kwargs)
        moment = datetime.now()
        if not self.last_data_update:
            self._update_data()
        elif moment - self.last_data_update > UPDATE_TIMES['data']:
            self._update_data()
        if not self.last_prices_update:
            self._update_prices()
        elif moment - self.last_prices_update > UPDATE_TIMES['prices']:
            self._update_prices()

    def _update_data(self):
        try:
            self._modified_attrs.append('data')
        except AttributeError:
            self._modified_attrs = ['data']
        print 'Update data'

    def _update_prices(self):
        try:    
            self._modified_attrs.append('prices')
        except AttributeError:
            self._modified_attrs = ['prices']
        print 'Update prices'

admin.site.register(Card)
