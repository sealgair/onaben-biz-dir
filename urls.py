"""
"""
from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^directory/', include('onaben.directory.urls')),
    url(r'^admin/(.*)', admin.site.root),
)

urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
)