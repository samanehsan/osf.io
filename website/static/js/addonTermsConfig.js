'use strict';
var $ = require('jquery');
var $osf = require('js/osfHelpers');

var ViewModel = function(urls, selector, userHasAuth) {
    var self = this;
    self.urls = urls;
    self.userHasAuth = userHasAuth;

    self.connectAccount = function() {
        if(userHasAuth) {
            return $osf.putJSON(self.urls().import, {});
        } else {
            $.ajax({
                url: self.urls().connect,
                type: 'GET',
                dataType: 'json'
            });
        }
    };
};

function AddonTerms(selector, urls, userHasAuth) {
    var self = this;
    self.urls = urls;
    self.viewModel = new ViewModel(urls, selector, userHasAuth);
    $osf.applyBindings(self.viewModel, selector);
}

module.exports = AddonTerms;
