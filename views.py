__author__ = 'jond'

import json

def getcontacts():

    contacts = [{'guid':1,
                 'firstName':'Jon',
                 'lastName':'Dunleavy',
                 'phoneNumbers':['(415) 555-2380']},
    ]

    return json.dumps({"contacts":contacts})
