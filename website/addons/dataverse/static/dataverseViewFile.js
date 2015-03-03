/**
 * Simple knockout model and view model for rendering the info table on the
 * file detail page.
 */

'use strict';
var ko = require('knockout');
require('knockout-punches');
var $ = require('jquery');
var $osf = require('osfHelpers');
var bootbox = require('bootbox');

ko.punches.enableAll();

function ViewModel(url) {
    var self = this;
    self.nodeTitle = ko.observable();
    self.filename = ko.observable();
    self.dataverse = ko.observable();
    self.dataverse_url = ko.observable();
    self.study = ko.observable();
    self.study_url = ko.observable();
    self.download_url = ko.observable();
    self.delete_url = ko.observable();
    self.files_url = ko.observable();
    self.loaded = ko.observable(false);
    self.deleting = ko.observable(false);

    // Note: Dataverse registrations not yet enabled
    self.registered = ko.observable(null);

    $.ajax({
        url: url, type: 'GET', dataType: 'json',
        success: function(response) {
            var data = response.data;
            self.nodeTitle(data.node.title);
            self.filename(data.filename);
            self.dataverse(data.dataverse);
            self.dataverse_url(data.urls.dataverse);
            self.study(data.study);
            self.study_url(data.urls.study);
            self.download_url(data.urls.download);
            self.delete_url(data.urls.delete);
            self.files_url(data.urls.files);
            self.loaded(true);
        }
    });

    self.deleteFile = function(){
        bootbox.confirm(
            {
                title: 'Delete Dataverse file?',
                message:'Are you sure you want to delete <strong>' +
                          self.filename() + '</strong> from your Dataverse?',
                callback: function(confirmed) {
                    if (confirmed) {
                        self.deleting(true);
                        var request = $.ajax({
                            type: 'DELETE',
                            url: self.delete_url()
                        });
                        request.done(function() {
                            window.location = self.files_url();
                        });
                        request.fail(function( jqXHR, textStatus ) {
                            self.deleting(false);
                            $osf.growl( 'Could not delete', textStatus );
                        });
                    }
                }
        });
    };
}

// Public API
function DataverseFileTable(selector, url) {
    this.viewModel = new ViewModel(url);
    $osf.applyBindings(this.viewModel, selector);
}

module.exports = DataverseFileTable;
