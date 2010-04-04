"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
        
from django.core.management import call_command
from django.db.models import loading
from django.test import TestCase
from django.conf import settings

class FakeModelTestCase(TestCase):
    """
    """
    
    def setUp(self):
        """
        """
        self.old_apps = settings.INSTALLED_APPS
        settings.INSTALLED_APPS.append("utils.tests")
        loading.cache.loaded = False
        call_command('syncdb', verbosity=0)
    
    def tearDown(self):
        """
        """
        settings.INSTALLED_APPS = self.old_apps
        loading.cache.loaded = False
        call_command('syncdb', verbosity=0)
