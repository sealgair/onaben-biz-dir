"""
Tests for directory app
"""
import string
from BeautifulSoup import BeautifulSoup

from django.test import TestCase
from django.core.urlresolvers import reverse

from directory.models import Category, Business
from directory.middleware import popular_categories
from django.conf import settings

class TestForms(TestCase):
    """
    Tests for directory forms
    """

class TestMiddleware(TestCase):
    """
    Tests for Directory middleware
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

def href_of(soup, id, attr='id'):
    """
    """
    node = soup.find('a', {attr: id})
    if node is None:
        return None
    else:
        return node.attrMap['href']

class FunctionalTests(TestCase):
    """
    Tests for Directory views
    """
    
    def setUp(self):
        """
        Create some tests businesses & categories
        """
        for b in range(3*settings.POPULAR_CATEGORY_COUNT): # 3 pages worth
            biz = Business.objects.create(name="business %s" % b)
            cat = Category.objects.create(name="category %s" % b)
            cat.businesses.add(biz)
            cat.save()
    
    def test_splash_page(self):
        """
        """
    
    def test_list_pages(self):
        """
        Test that each list page shows first/prev/next/last links 
        where applicable, with the correct url in each
        """
        for show_by in ['businesses', 'categories']:
            def url_for(page=None):
                if page:
                    return reverse('list', kwargs={'show_by': show_by, 'page': page})
                else:
                    return reverse('list', kwargs={'show_by': show_by})
            
            base_url = url_for()
            base_response = self.client.get(base_url)
            
            url = url_for(1)
            response = self.client.get(url)
            self.assertEquals(base_response.content, response.content)
            
            last_page = 3
            
            seen = 0
            while url is not None:
                response = self.client.get(url)
                seen += 1
                
                soup = BeautifulSoup(response.content)
                if seen == 1:
                    self.assertNotContains(response, 'id="first-page"')
                    self.assertNotContains(response, 'id="prev-page"')
                else:
                    self.assertEqual(url_for(), href_of(soup, 'first-page'))
                    self.assertEqual(url_for(seen-1), href_of(soup, 'prev-page'))
                
                if seen == last_page:
                    self.assertNotContains(response, 'id="last-page"')
                    self.assertNotContains(response, 'id="next-page"')
                else:
                    self.assertEqual(url_for(last_page), href_of(soup, 'last-page'))
                    self.assertEqual(url_for(seen+1), href_of(soup, 'next-page'))
                
                url = href_of(soup, 'next-page')
    
    def test_list_businesses(self):
        """
        Test that each business list page displays the correct number of
        business (and category) links with the correct url in each.
        """
        response = self.client.get("/directory/businesses/")
        soup = BeautifulSoup(response.content)
        self.assertEqual(10, len(soup.findAll('a', 'item-link')))
        self.assertEqual(10, len(soup.findAll('a', 'sub-item-link')))
        
        for i, node in enumerate(soup.findAll(None, "item-data")):
            biz = Business.objects.all()[i]
            self.assertEqual(href_of(node, 'item-link', attr='class'), biz.get_absolute_url())
            cat = biz.categories.get()
            self.assertEqual(href_of(node, 'sub-item-link', attr='class'), cat.get_absolute_url())
            
        
    def test_list_categories(self):
        """
        Test that each category list page displays the correct number of
        category links with the correct url in each.
        """
        response = self.client.get("/directory/categories/")
        soup = BeautifulSoup(response.content)
        self.assertEqual(10, len(soup.findAll('a', 'item-link')))
        self.assertEqual(0, len(soup.findAll('a', 'sub-item-link')))
        
        for i, node in enumerate(soup.findAll(None, "item-data")):
            cat = Category.objects.all()[i]
            self.assertEqual(href_of(node, 'item-link', attr='class'), cat.get_absolute_url())
            self.assertEqual(u'1', node.find(None, {'class': 'biz-count'}).contents[0])
    
    def test_detail_view(self):
        """
        """
    
    def test_register(self):
        """
        """