__author__ = 'jond'

import re

import views

REDIRECTS = ((re.compile('contacts.json'), views.getcontacts),
             (re.compile('contact/add.json'), views.addcontact))