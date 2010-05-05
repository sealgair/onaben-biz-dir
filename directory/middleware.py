"""
"""
import sys
from django.db.models import Count
from django.conf import settings
from django.views.debug import technical_500_response

from directory.models import Category

def popular_categories(request):
    """
    Add a list of popular categories to the context
    """
    context = {}
    
    popcats = Category.objects.annotate(biz_num=Count('businesses')).order_by('-biz_num')
    context['popcats'] = popcats[:settings.POPULAR_CATEGORY_COUNT]
    
    return context

def default_show_by(request):
    """
    Add default 'show_by' param to context if it's not there already
    """
    context = {}
    
    if 'show_by' not in context or not context['show_by']:
        context['show_by'] = 'business'
    
    return context

class UserBasedExceptionMiddleware(object):
    """
    Source: http://ericholscher.com/blog/2008/nov/15/debugging-django-production-environments/
    
    Introduction
    ------------
    This is a pretty simple middleware that is crazy useful. When you throw this
    inside of your site, it will give you a normal Django error page if
    you're a superuser, or if your IP is in INTERNAL_IPS.
    
    Implement
    ---------
    Add to your middleware:
    
    'sugar.middleware.debugging.UserBasedExceptionMiddleware',
    
    """

    def process_exception(self, request, exception):
        if request.user.is_superuser or request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS:
            return technical_500_response(request, *sys.exc_info())
