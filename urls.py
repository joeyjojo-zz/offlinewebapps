__author__ = 'jond'

import re

import views

REDIRECTS = ((re.compile('contacts'), views.getcontacts),
             (re.compile('contact/add.json'), views.addcontact))