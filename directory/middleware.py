"""
"""
from django.db.models import Count
from directory.models import Category
from django.conf import settings

def popular_categories(request):
    """
    Add a list of popular categories to the context
    """
    context = {}
    
    popcats = Category.objects.annotate(biz_num=Count('business')).order_by('-biz_num')
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