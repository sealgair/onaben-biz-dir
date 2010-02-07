"""
"""

from haystack import indexes
from haystack import site

from directory.models import Business, Category

class BusinessIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)

class CategoryIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)

site.register(Business, BusinessIndex)
#site.register(Category, CategoryIndex)
