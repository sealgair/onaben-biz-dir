"""
"""
from django.test import TestCase

from directory.models import Category, Business
from directory.middleware import popular_categories
from django.conf import settings

class TestForms(TestCase):
    """
    """

class TestMiddleware(TestCase):
    """
    """
    
    def test_popular_categories(self):
        """
        Assert that popular_categories returns a correctly ordered list of the categories
        with the most businesses attached, with biz_num set to the correct value
        """
        cats = []
        for c in range(30):
            cat = Category.objects.create(name="test category %s" % c)
            for b in range(c):
                biz, created = Business.objects.get_or_create(name="test business %s" % b)
                cat.businesses.add(biz)
                cat.save()
            if 30-settings.POPULAR_CATEGORY_COUNT <= c:
                cats.insert(0, cat)
        
        context = popular_categories(None)
        popcats = context['popcats']
        self.assertEqual(settings.POPULAR_CATEGORY_COUNT, len(popcats))
        for expected, found in zip(cats, popcats):
            self.assertEqual(expected, found)
            self.assertEqual(found.name, "test category %s" % found.biz_num, )

class FunctionalTests(TestCase):
    """
    """
    
    def test_list_view(self):
        """
        """
    
    def test_detail_view(self):
        """
        """
    
    def test_register(self):
        """
        """