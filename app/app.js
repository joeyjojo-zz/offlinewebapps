App = Ember.Application.create({ ready: function() { App.contactsController.findAll() }});


App.store = DS.Store.create({
    revision: 4,
    adapter: DS.RESTAdapter.create({ bulkCommit: false })
});

App.Contact  = DS.Model.extend({
    firstName: DS.attr('string'),
    lastName:  DS.attr('string'),

    hasName: function() {
        console.log("check name!");
        var firstName = this.get('firstName'),
            lastName = this.get('lastName');
        console.log(firstName);
        console.log(lastName);
        return firstName !== '' || lastName !== '';
    }.property('firstName', 'lastName'),

    // This value is used to determine how the contact
    // should be sorted in the contacts list. By default
    // we sort by last name, but we use the first name if
    // no last name is provided.
    sortValue: function() {
        return this.get('lastName') || this.get('firstName');
    }.property('firstName', 'lastName'),

    validate: function() {
        if (this.get('firstName') === undefined || this.get('firstName') === '' ||
            this.get('lastName') === undefined  || this.get('lastName') === '') {
            return 'Contacts require a first and a last name.';
        }
    },

    fullName: Em.computed(function() {
        return this.get('firstName') + ' ' + this.get('lastName');
    }).property('firstName', 'lastName')
});

App.Contact.reopenClass({
    collectionUrl: '/contacts',
    resourceUrl: '/contact/%@',
    resourceName: 'contact'
});

App.contactsController = Ember.ArrayProxy.create({
    // The array of Contact objects that backs the array controller.
    content: [],

    findAll: function() {
        console.log(App.store.findAll(App.Contact));
        this.set('content', App.store.findAll(App.Contact));
    }
});

App.ContactListView = Ember.View.extend({
    classNameBindings: ['isSelected'],

    click: function() {
        var content = this.get('content');

        App.selectedContactController.set('content', content);
    },

    touchEnd: function() {
        this.click();
    }/*,

    isSelected: function() {
        var selectedItem = App.selectedContactController.get('content'),
            content = this.get('content');

        if (content === selectedItem) { return true; }
    }.property('App.selectedContactController.content')
    */
});

