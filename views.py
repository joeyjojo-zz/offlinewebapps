__author__ = 'jond'

import json

import models

"""
Contact views
"""
def getcontacts(id=None):
    """
    Retrieves all the contacts currently stored in the database
    @return: unicode
    """
    if id is None:
        contacts = [{'id':c.id,
                     'firstName':c.firstName,
                     'lastName':c.lastName or "",
                     'phoneNumbers':[pn.number for pn in c.phonenumber]
                    } for c in models.Contact.query.all()]
        return json.dumps({"contacts":contacts})
    else:
        c = models.Contact.query.filter_by(id=id).one()
        r = [{'id':c.id,
                'firstName':c.firstName,
                'lastName':c.lastName or "",
                'phoneNumbers':[pn.number for pn in c.phonenumber]
        }]
        return json.dumps({"contacts":r})

def addcontact(firstName, lastName):
    """
    Add a contact to the database
    @param firstName: The first name of the contact
    @type firstName: unicode
    @param lastName: The last name of the contact (surname)
    @type lastName: unicode
    """
    c = models.Contact(firstName=firstName,
                       lastName=lastName)
    models.session.commit()
    return json.dumps({"success":True})

def editcontact(guid, firstName=None, lastName=None):
    """
    Edit the contact specified by guid
    @param guid: The id of the contact in the database
    @type guid: int
    @param firstName: The value to change the first name to
    @type firstName: unicode
    @param lastName: The value to change the last name to
    @type lastName: unicode
    """
    c = models.Contact.get(guid)
    if firstName is not None:
        c.firstName = firstName
    if lastName is not None:
        c.lastName = lastName
    models.session.commit()
    return json.dumps({"success":True})

def deletecontact(guid):
    """
    Delete the specified contact
    @param guid: The id of the contact in the database
    @type guid: int
    """
    c = models.Contact.get(guid)
    c.delete()
    models.session.commit()
    return json.dumps({"success":True})

"""
Phonenumber views
"""