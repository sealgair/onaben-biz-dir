"""
"""
from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.views.generic.simple import redirect_to
from django.core.urlresolvers import reverse
from django.utils.functional import lazy
reverse = lazy(reverse, type(''))

from django.contrib import admin
admin.autodiscover()

from haystack.views import basic_search
from haystack.forms import SearchForm

urlpatterns = patterns('',
    url(r'^directory/', include('directory.urls')),
    #url(r'^search/', include('haystack.urls')),
    url(r'^search/', basic_search, dict(form_class=SearchForm), name='search'),
    url(r'^admin/(.*)', admin.site.root),
    url(r'^$', redirect_to, {'url': reverse('splash')}),
)

urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
)