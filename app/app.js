App = Ember.Application.create();

App.store = DS.Store.create({
    revision: 4,
    adapter: DS.RESTAdapter.create({ bulkCommit: false })
});

App.Contact = DS.Model.extend({
    firstName: DS.attr('string'),
    lastName: DS.attr('string'),

    hasName: function() {
        var firstName = this.get('firstName'),
            lastName = this.get('lastName');

        return firstName !== '' || lastName !== '';
    }.property('firstName', 'lastName'),

    // This value is used to determine how the contact
    // should be sorted in the contacts list. By default
    // we sort by last name, but we use the first name if
    // no last name is provided.
    sortValue: function() {
        return this.get('lastName') || this.get('firstName');
    }.property('firstName', 'lastName')
});

App.contactsController = Ember.ArrayController.create({
    // The array of Contact objects that backs the array controller.
    content: App.store.findAll(App.Contact)
})