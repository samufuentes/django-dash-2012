from django.db import models
from django_hstore import hstore
from django.contrib import admin
from django.utils.encoding import smart_str
from datetime import datetime, timedelta
from card.sql import CARD_SEARCH_QUERY as card_query
from card.utils import get_link

UPDATE_TIMES = {
    'prices': timedelta(hours=1),
    'data': timedelta(days=1),
    }

class Card(models.Model):
    _data = hstore.DictionaryField()
    last_data_update = models.DateTimeField()
    _prices = hstore.DictionaryField()
    last_prices_update = models.DateTimeField()

    objects = hstore.HStoreManager()

    def __unicode__(self):
        card = "Card %s (updated %s)" % (str(self._data), 
                    self.last_data_update)
        prices = "Prices %s (updated %s)" % (str(self._prices), 
                    self.last_prices_update)
        return "%s\n%s" % (card, prices)

    def set_data(self, value):
        self._data = self.prepare_hstore(value)
        self.last_data_update = datetime.now()

    def get_data(self):
        if datetime.now() - self.last_data_update > UPDATE_TIMES['data']:
            self._update_data()
        if not self._data.get('link') and 'id' in self._data:
            self._data['link'] = get_link(self._data['id'])
            self.save()
        return self.load_hstore(self._data)

    data = property(get_data, set_data)

    def set_prices(self, value):
        self._prices = self.prepare_hstore(value)
        self.last_prices_update = datetime.now()

    def get_prices(self):
        if datetime.now() - self.last_prices_update > UPDATE_TIMES['prices']:
            self._update_prices()
        return self.load_hstore(self._prices)

    prices = property(get_prices, set_prices)

    def _update_data(self):
        self.last_data_update = datetime.now()
        print 'Update data'

    def _update_prices(self):
        self.last_prices_update = datetime.now()
        print 'Update prices'

    @classmethod
    def freesearch(cls, text):
        splitted = text.split(' ')
        return cls.objects.raw(card_query, (splitted, len(splitted)))


    def load_hstore(self, value):
        for key in value:
            if '&' in value[key] and key != 'link':
                value[key] = value[key].split('&')
                while value[key][-1] == '':
                    value[key] = value[key][:-1]
        return value

    def prepare_hstore(self, value):
        for key in value:
            if isinstance(value[key], list):
                value[key] = '&'.join([smart_str(v) for v in value[key]])
                if '&' not in value[key]:
                    value[key] = value[key] + '&'
            value[key] = smart_str(value[key])
        return value

admin.site.register(Card)
