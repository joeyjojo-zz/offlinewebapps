__author__ = 'jond'

from elixir import *

metadata.bind = "sqlite:///contacts.sqlite"
metadata.bind.echo = True

class Contact(Entity):
    firstname = Field(Unicode(100))
    lastname = Field(Unicode(100))
    phonenumber = OneToMany("PhoneNumber")

    def __repr__(self):
        return '<Contact "{0}" (%d)>'.format(self.name)

class PhoneNumber(Entity):
    contact = ManyToOne("Contact")
    number = Field(Unicode(15))

    def __repr__(self):
        return '<PhoneNmber "{0}" (%d)>'.format(self.number)

def loadfixtures():
    c = Contact(firstname="jimmy",
                lastname="bob bluh",
                phonenumber=[PhoneNumber(number="(123) 4567890")])
    session.commit()