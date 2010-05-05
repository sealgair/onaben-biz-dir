import os
import sys
import site

PROJECT_ROOT = os.path.dirname(__file__) #.../onaben/src/onaben
PROJECT_ROOT = os.path.dirname(PROJECT_ROOT) #.../onaben/src
PROJECT_ROOT = os.path.dirname(PROJECT_ROOT) #.../onaben

sys.path.append(PROJECT_ROOT+'/src')
sys.path.append(PROJECT_ROOT+'/src/onaben')
site.addsitedir(PROJECT_ROOT+'/lib/python2.4/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = 'onaben.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
