__author__ = 'jond'

import json

import models

def getcontacts():

    contacts = [{'guid':c.id,
                 'firstName':c.firstName,
                 'lastName':c.lastName or "",
                 'phoneNumbers':[pn.number for pn in c.phonenumber]} for c in models.Contact.query.all()]

    return json.dumps({"contacts":contacts})

def addcontact(firstName, lastName):
    c = models.Contact(firstName=firstName,
                       lastName=lastName)
    models.session.commit()
    return json.dumps({"success":True})