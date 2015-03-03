/**
 * Module that controls the Dropbox node settings. Includes Knockout view-model
 * for syncing data, and HGrid-folderpicker for selecting a folder.
 */
    'use strict';

    var ko = require('knockout');
    require('knockout-punches');
    var $ = require('jquery');
    var bootbox = require('bootbox');
    var Raven = require('raven-js');

    var FolderPicker = require('folderpicker');
    var ZeroClipboard = require('zeroclipboard');
    ZeroClipboard.config('/static/vendor/bower_components/zeroclipboard/dist/ZeroClipboard.swf');
    var $osf = require('osfHelpers');

    ko.punches.enableAll();
/**
 * Knockout view model for the Figshare node settings widget.
 */
var ViewModel = function(url, selector, folderPicker) {
    var self = this;
    // Auth information
    self.nodeHasAuth = ko.observable(false);
    self.userHasAuth = ko.observable(false);
    self.userIsOwner = ko.observable(false);
    // Currently linked folder, an Object of the form {name: ..., path: ...}
    self.linked = ko.observable({});
    self.ownerName = ko.observable('');
    self.urls = ko.observable({});
    // Flashed messages
    self.message = ko.observable('');
    self.messageClass = ko.observable('text-info');
    // Display names
    self.PICKER = 'picker';
    self.SHARE = 'share';
    // Current folder display
    self.currentDisplay = ko.observable(null);
    // CSS selector for the folder picker div
    self.folderPicker = folderPicker;
    // Currently selected folder, an Object of the form {name: ..., path: ...}
    self.selected = ko.observable(null);
    // Emails of contributors, can only be populated by activating the share dialog
    self.loading = ko.observable(false);
    // Whether the initial data has been fetched form the server. Used for
    // error handling.
    self.loadedSettings = ko.observable(false);
    // Whether the contributor emails have been loaded from the server
    self.disableShare = ko.computed(function() {
        return !self.urls().share;
    });
    /**
     * Update the view model from data returned from the server.
     */
    self.updateFromData = function(data) {
        self.ownerName(data.ownerName);
        self.nodeHasAuth(data.nodeHasAuth);
        self.userHasAuth(data.userHasAuth);
    self.userIsOwner(data.userIsOwner);
    self.linked(data.linked || {});
        self.urls(data.urls);
    };

    self.fetchFromServer = function() {
        $.ajax({
            url: url, type: 'GET', dataType: 'json',
            success: function(response) {
                self.updateFromData(response.result);
                self.loadedSettings(true);
            },
            error: function(xhr, textStatus, error) {
                self.changeMessage('Could not retrieve Figshare settings at ' +
                    'this time. Please refresh ' +
                    'the page. If the problem persists, email ' +
                    '<a href="mailto:support@osf.io">support@osf.io</a>.',
                    'text-warning');
                Raven.captureMessage('Could not GET Figshare settings', {
                    url: url,
                    textStatus: textStatus,
                    error: error
                });
            }
        });
    };

    // Initial fetch from server
    self.fetchFromServer();

    /**
     * Whether or not to show the Import Access Token Button
     */
    self.showImport = ko.computed(function() {
        // Invoke the observables to ensure dependency tracking
        var userHasAuth = self.userHasAuth();
        var nodeHasAuth = self.nodeHasAuth();
        var loaded = self.loadedSettings();
        return userHasAuth && !nodeHasAuth && loaded;
    });

    /** Whether or not to show the full settings pane. */
    self.showSettings = ko.computed(function() {
        return self.nodeHasAuth();
    });

    /** Whether or not to show the Create Access Token button */
    self.showTokenCreateButton = ko.computed(function() {
        // Invoke the observables to ensure dependency tracking
        var userHasAuth = self.userHasAuth();
        var nodeHasAuth = self.nodeHasAuth();
        var loaded = self.loadedSettings();
        return !userHasAuth && !nodeHasAuth && loaded;
    });

    /** Computed functions for the linked and selected folders' display text.*/

    self.folderName = ko.computed(function() {
        // Invoke the observables to ensure dependency tracking
        var nodeHasAuth = self.nodeHasAuth();
        var linked = self.linked();
        return (nodeHasAuth && linked)? linked.title : '';
    });

    self.selectedFolderName = ko.computed(function() {
        var userIsOwner = self.userIsOwner();
        var selected = self.selected();
        return (userIsOwner && selected) ? selected.title : '';
    });

    self.selectedFolderType = ko.computed(function(){
        var userHasAuth = self.userHasAuth();
            var selected = self.selected();
            return (userHasAuth && selected) ? selected.type : '';
    });

    function onSubmitSuccess(response) {
        self.changeMessage('Successfully linked "' + $osf.htmlEscape(self.selected().title) +
            '". Go to the <a href="' +
            self.urls().files + '">Files page</a> to view your files.',
            'text-success', 5000);
        // Update folder in ViewModel
        self.linked(response.result.linked);
        self.urls(response.result.urls);
        self.cancelSelection();
    }

    function onSubmitError() {
        self.changeMessage('Could not change settings. Please try again later.', 'text-danger');
    }

    /**
     * Send a PUT request to change the linked Figshare folder.
     */
    self.submitSettings = function() {
        $osf.putJSON(self.urls().config, ko.toJS(self))
            .done(onSubmitSuccess)
            .fail(onSubmitError);
    };

    /**
     * Must be used to update radio buttons and knockout view model simultaneously
     */
    self.cancelSelection = function() {
        self.selected(null);
        // $(selector + ' input[type="radio"]').prop('checked', false);
    };

    /** Change the flashed message. */
    self.changeMessage = function(text, css, timeout) {
        self.message(text);
        var cssClass = css || 'text-info';
        self.messageClass(cssClass);
        if (timeout) {
            // Reset message after timeout period
            setTimeout(function() {
                self.message('');
                self.messageClass('text-info');
            }, timeout);
        }
    };

    /**
     * Send DELETE request to deauthorize this node.
     */
    function sendDeauth() {
        return $.ajax({
            url: self.urls().deauthorize,
            type: 'DELETE',
            success: function() {
                // Update observables
                self.nodeHasAuth(false);
                self.cancelSelection();
                self.currentDisplay(null);
                self.changeMessage('Deauthorized Figshare.', 'text-warning', 3000);
            },
            error: function() {
                self.changeMessage('Could not deauthorize because of an error. Please try again later.',
                    'text-danger');
            }
        });
    }

    /** Pop up a confirmation to deauthorize Figshare from this node.
     *  Send DELETE request if confirmed.
     */
    self.deauthorize = function() {
        bootbox.confirm({
            title: 'Deauthorize Figshare?',
            message: 'Are you sure you want to remove this Figshare authorization?',
            callback: function(confirmed) {
                if (confirmed) {
                    return sendDeauth();
                }
            }
        });
    };

    // Callback for when PUT request to import user access token
    function onImportSuccess(response) {
        var msg = response.message || 'Successfully imported access token from profile.';
        // Update view model based on response
        self.changeMessage(msg, 'text-success', 3000);
        self.updateFromData(response.result);
        self.activatePicker();
    }

    function onImportError() {
        self.message('Error occurred while importing access token.');
        self.messageClass('text-danger');
    }

    /**
     * Send PUT request to import access token from user profile.
     */
    self.importAuth = function() {
        bootbox.confirm({
            title: 'Import Figshare Access Token?',
            message: 'Are you sure you want to authorize this project with your Figshare access token?',
            callback: function(confirmed) {
                if (confirmed) {
                    return $osf.putJSON(self.urls().importAuth, {})
                        .done(onImportSuccess)
                        .fail(onImportError);
                }
            }
        });
    };

    /** Callback for chooseFolder action.
    *   Just changes the ViewModel's self.selected observable to the selected
    *   folder.
    */
        function onPickFolder(evt, item) {
            evt.preventDefault();
            self.selected({title: item.data.name, type: item.data.type, id: item.data.id});
            return false; // Prevent event propagation
        }

    /**
     * Activates the HGrid folder picker.
     */
    self.activatePicker = function() {
        self.currentDisplay(self.PICKER);
        // Show loading indicator
        self.loading(true);
        $(self.folderPicker).folderpicker({
            onPickFolder: onPickFolder,
            initialFolderName : self.folderName(),
            initialFolderPath : undefined,
            // Fetch Figshare folders with AJAX
            filesData: self.urls().options, // URL for fetching folders
            // Lazy-load each folder's contents
            // Each row stores its url for fetching the folders it contains
            resolveLazyloadUrl : function(tree, item){
                return item.data.urls.fetch;
            },
            oddEvenClass : {
                odd : 'figshare-folderpicker-odd',
                even : 'figshare-folderpicker-even'
            },
            ajaxOptions: {
               error: function(xhr, textStatus, error) {
                    self.loading(false);
                    self.changeMessage('Could not connect to Figshare at this time. ' +
                                        'Please try again later.', 'text-warning');
                    Raven.captureMessage('Could not GET Figshare contents', {
                        textStatus: textStatus,
                        error: error
                    });
                }
            },
            folderPickerOnload: function() {
                // Hide loading indicator
                self.loading(false);
            }
        });
    };

    /**
     * Toggles the visibility of the folder picker.
     */
    self.togglePicker = function() {
        // Toggle visibility of folder picker
        var shown = self.currentDisplay() === self.PICKER;
        if (!shown) {
            self.currentDisplay(self.PICKER);
            self.activatePicker();
        } else {
            self.currentDisplay(null);
            // Clear selection
            self.cancelSelection();
        }
    };
};

// Public API
function FigshareNodeConfig(selector, url, folderPicker) {
    var self = this;
    self.url = url;
    self.folderPicker = folderPicker;
    self.viewModel = new ViewModel(url, selector, folderPicker);
    $osf.applyBindings(self.viewModel, selector);
}

module.exports = FigshareNodeConfig;

