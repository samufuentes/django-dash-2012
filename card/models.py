from django.db import models
from django_hstore import hstore
from django.contrib import admin

class Card(models.Model):
    data = hstore.DictionaryField()
    objects = hstore.HStoreManager()

    def __unicode__(self):
        return str(self.data)

admin.site.register(Card)
