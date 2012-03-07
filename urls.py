__author__ = 'jond'

import re

import views

REDIRECTS = ((re.compile('contacts.json'), views.getcontacts),)