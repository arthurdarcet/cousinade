from django.conf import settings
from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'static/(?P<path>.*)', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^$', 'cousinade.views.index'),
    url(r'^tree$', 'cousinade.views.tree'),
    url(r'^search/(.+)$', 'cousinade.views.search'),
    url(r'^add/?$', 'cousinade.views.edit'),
    url(r'^edit/([0-9]+)$', 'cousinade.views.edit'),
    url(r'^login$', 'cousinade.views.login'),
    url(r'^logout$', 'cousinade.views.logout'),
    url(r'^password/request/?$', 'cousinade.views.request_password_reset'),
    url(r'^password/do/?$', 'cousinade.views.do_password_reset'),
    url(r'^password/do/(?P<uidb36>.*)/(?P<token>.*)$', 'cousinade.views.do_password_reset'),
)
