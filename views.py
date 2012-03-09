__author__ = 'jond'

import json

import models

def getcontacts():

    contacts = [{'guid':c.id,
                 'firstName':c.firstname,
                 'lastName':c.lastname,
                 'phoneNumbers':[pn.number for pn in c.phonenumber]} for c in models.Contact.query.all()]

    return json.dumps({"contacts":contacts})

def addcontact(firstname, surname):
    print "adding contact!", firstname, surname
    return json.dumps({"success":True})