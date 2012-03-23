window.App = Ember.Application.create();

App.store = DS.Store.create({
    revision: 4,
    adapter: DS.RESTAdapter.create({namespace: "http://testing"})
});

App.Contact = DS.Model.extend({
    firstName: DS.attr('string')
});

App.contactsController = Ember.ArrayProxy.create({
    content: App.store.findAll(App.Contact)
});