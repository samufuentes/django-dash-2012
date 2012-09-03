from django.conf.urls import patterns, include, url
from card.api import CardResource

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# API resources
card_resource = CardResource()
print card_resource.urls
print "lll"

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'voidring.views.home', name='home'),
    url(r'^cards/$', 'voidring.views.cards'),
    url(r'^cards/(\d*)/$', 'voidring.views.card_detail'),
    url(r'^cards/statistics/', 'voidring.views.card_statistics'),
    url(r'^search/$', 'voidring.views.search_card'),
    # url(r'^voidring/', include('voidring.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    #(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    # Django facebook
    #(r'^facebook/', include('django_facebook.urls')),
    #(r'^accounts/', include('django_facebook.auth_urls')), #Don't add this line if you use django registration or userena for registration and auth.
    # Django registration
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^api/', include(card_resource.urls)),
)
