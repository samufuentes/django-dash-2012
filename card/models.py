from django.db import models
from django_hstore import hstore

class Card(models.Model):
    data = hstore.DictionaryField()
    objects = hstore.HStoreManager()

    def __unicode__(self):
        return str(self.data)
