from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('cousinade.views',
    url(r'static/(?P<path>.*)', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'index', name='index'),
    url(r'^listing$', 'listing', name='listing'),
)
