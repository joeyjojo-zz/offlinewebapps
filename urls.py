__author__ = 'jond'

import re
import views

REDIRECTS = ((re.compile(r'contacts'), views.getcontacts),
             (re.compile(r'contact/(?P<id>[\d]+)'), views.getcontacts),
             (re.compile('contact/add'), views.addcontact))