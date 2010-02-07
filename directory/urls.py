"""
"""

from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template

parts = {}
parts['type'] = r'(?P<show_by>\w*)'
parts['name'] = r'(?P<name>.*)'
parts['alpha'] = r'letter/(?P<alpha>[A-Z])'
parts['page'] = r'(?P<page>[0-9]*)'

urlpatterns = patterns('onaben.directory.views',
    url(r'^$', direct_to_template, dict(template="directory/splash.html"), name="splash"),
    url(r'^welcome$', direct_to_template, dict(template="directory/splash.html"), name="splash"),
    
    url(r'^register/?$', 'register', name='register'),
    
    url(r'^{type}/?$'.format(**parts), 'show_list', name='list'),
    url(r'^{type}/{page}$'.format(**parts), 'show_list', name='list'),
    url(r'^{type}/{alpha}$'.format(**parts), 'show_list', name='list'),
    url(r'^{type}/{alpha}/{page}$'.format(**parts), 'show_list', name='list'),
    url(r'^{type}/name={name}$'.format(**parts), 'show_detail', name='one'),
)

urlpatterns += patterns('',
    url(r'^(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/home/chase/Documents/Code/django/dvrc/templates/media'}),
)
