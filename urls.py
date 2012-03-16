__author__ = 'jond'

import re

import views

REDIRECTS = ((re.compile('contact'), views.getcontacts),
             (re.compile('contact/add.json'), views.addcontact))