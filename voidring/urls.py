from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'voidring.views.home', name='home'),
    url(r'^cards/$', 'voidring.views.cards'),
    url(r'^cards/statistics/', 'voidring.views.card_statistics'),
    # url(r'^voidring/', include('voidring.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # Django facebook
    (r'^facebook/', include('django_facebook.urls')),
    (r'^accounts/', include('django_facebook.auth_urls')), #Don't add this line if you use django registration or userena for registration and auth.
    # Django registration
    (r'^accounts/', include('registration.backends.default.urls')),
)
