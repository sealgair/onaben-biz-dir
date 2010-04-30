import os
import sys
import site

sys.path.append('/www/onaben/src')
sys.path.append('/www/onaben/src/onaben')
site.addsitedir('/www/onaben/lib/python2.4/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = 'onaben.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
