__author__ = 'jond'

from elixir import *

metadata.bind = "sqlite:///contacts.sqlite"
metadata.bind.echo = True

class Contact(Entity):
    firstName = Field(Unicode(100))
    lastName = Field(Unicode(100))
    phonenumber = OneToMany("PhoneNumber")

    def __repr__(self):
        return '<Contact "{0}" (%d)>'.format(self.firstName)

class PhoneNumber(Entity):
    contact = ManyToOne("Contact")
    number = Field(Unicode(15))

    def __repr__(self):
        return '<PhoneNmber "{0}" (%d)>'.format(self.number)
