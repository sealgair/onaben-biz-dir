"""
"""

from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('onaben.directory.views',
    url(r'^$', direct_to_template, dict(template="directory/splash.html"), name="splash"),
    url(r'^welcome$', direct_to_template, dict(template="directory/splash.html"), name="splash"),
    
    url(r'^register/?$', 'register', name='register'),
    
    url(r'^(?P<show_by>(?:businesses|categories))/?$', 'show_list', name='list'),
    url(r'^(?P<show_by>(?:businesses|categories))/(?P<page>(?:\d+|\w))/$', 'show_list', name='list'),
    url(r'^(?P<show_by>(?:business|category))/(?P<name>.*)/$', 'show_detail', name='one'),
)

urlpatterns += patterns('',
    url(r'^(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/home/chase/Documents/Code/django/dvrc/templates/media'}),
)
