'use strict';

var $ = require('jquery');
var m = require('mithril');
var Treebeard = require('treebeard');
var citations = require('./citations');

var apaStyle = require('raw!styles/apa.csl');

require('../vendor/bower_components/treebeard/dist/treebeard.css');
require('../css/fangorn.css');

function resolveToggle(item) {
    var toggleMinus = m('i.icon-minus', ' ');
    var togglePlus = m('i.icon-plus', ' ');
    if (item.kind === 'folder') {
        return item.open ? toggleMinus : togglePlus;
    } else {
        return '';
    }
}

function resolveIcon(item) {
    var privateFolder = m('img', {
        src: '/static/img/hgrid/fatcowicons/folder_delete.png'
    });
    var openFolder = m('i.icon-folder-open', ' ');
    var closedFolder = m('i.icon-folder-close', ' ');

    if (item.kind === 'folder') {
        return item.open ? openFolder : closedFolder;
    } else if (item.data.icon) {
        return m('i.fa.' + item.data.icon, ' ');
    } else {
        return m('i.icon-file-alt');
    }
}

var utils = {
    reduce: function(array, dst, fn) {
        for (var i = 0; i < array.length; i++) {
            fn(array[i], dst);
        }
        return dst;
    },
    zip: function(array1, array2) {
        var zipped = [];
        var min = Math.min(array1.length, array2.length);
        for (var i = 0; i < min; i++) {
            zipped.push([array1[i], array2[i]]);
        }
        return zipped;
    }
};

var objectify = function(array, key) {
    key = key || 'id';
    return utils.reduce(
        array, {},
        function(item, acc) {
            return acc[item[key]] = item;
        }
    );
};

var formatResult = function(state) {
    return '<div class="citation-result-title">' + state.title + '</div>';
};

var formatSelection = function(state) {
    return state.title;
};

var makeButtons = function(item, col, buttons) {
    return buttons.map(function(button) {
        var self = this;
        return m(
            'span', {
                'data-col': item.id
            }, [
                m(
                    'i', {
                        title: button.tooltip,
                        style: button.style,
                        'class': button.css,
                        'data-toggle': 'tooltip',
                        'data-placement': 'bottom',
                        'onclick': function(event) {
                            button.onclick.call(self, event, item, col);
                        }
                    }, [
                        m(
                            'span', {
                                class: button.icon
                            },
                            button.name
                        )
                    ]
                )
            ]
        );
    });
};

var buildExternalUrl = function(csl) {
    if (csl.DOI) {
        return 'http://dx.doi.org/' + csl.DOI;
    } else if (csl.PMID) {
        return 'http://www.ncbi.nlm.nih.gov/pubmed/' + csl.PMID;
    }
    return null;
};

var renderActions = function(item, col) {
    var self = this;
    var buttons = [];
    if (item.kind === 'item') {
        // Add link to external document
        var externalUrl = buildExternalUrl(item.data.csl);
        if (externalUrl) {
            buttons.push({
                name: '',
                css: 'btn btn-info btn-xs',
                icon: 'icon-external-link',
                tooltip: 'View original document',
                onclick: function(event) {
                    window.open(externalUrl);
                }
            });
        }
        // Add link to document on reference management service
        if (item.data.serviceUrl) {
            buttons.push({
                name: '',
                css: 'btn btn-info btn-xs',
                icon: 'icon-link',
                tooltip: 'View on ' + self.provider,
                onclick: function(event) {
                    window.open(item.data.serviceUrl);
                }
            });
        }
    }
    return makeButtons(item, col, buttons);
};

var treebeardOptions = {
    lazyLoad: true,
    showFilter: false,
    resolveIcon: resolveIcon,
    resolveToggle: resolveToggle,
    lazyLoadPreprocess: function(res) {
        return res.contents;
    },
    columnTitles: function() {
        return [{
            title: 'Citation',
            width: '80%',
            sort: false
        }, {
            title: 'Actions',
            width: '20%',
            sort: false
        }];
    }
};

var CitationGrid = function(provider, gridSelector, styleSelector, apiUrl) {
    var self = this;

    self.provider = provider;
    self.gridSelector = gridSelector;
    self.styleSelector = styleSelector;
    self.apiUrl = apiUrl;

    self.style = apaStyle;
    self.bibliographies = {};

    self.initTreebeard();
    self.initStyleSelect();
};

CitationGrid.prototype.initTreebeard = function() {
    var self = this;
    var options = $.extend({
            divID: self.gridSelector.replace('#', ''),
            filesData: self.apiUrl,
            resolveLazyloadUrl: function(item) {
                return item.data.urls.fetch;
            },
            // Wrap callback in closure to preserve intended `this`
            resolveRows: function() {
                return self.resolveRowAux.call(self, arguments);
            },
        },
        treebeardOptions
    );
    self.treebeard = new Treebeard(options);
};

CitationGrid.prototype.initStyleSelect = function() {
    var self = this;
    var $input = $(self.styleSelector);
    $input.select2({
        allowClear: true,
        formatResult: formatResult,
        formatSelection: formatSelection,
        placeholder: 'Citation Style (e.g. "APA")',
        minimumInputLength: 1,
        ajax: {
            url: '/api/v1/citations/styles/',
            quietMillis: 200,
            data: function(term, page) {
                return {
                    q: term
                };
            },
            results: function(data, page) {
                return {
                    results: data.styles
                };
            },
            cache: true
        }
    }).on('select2-selecting', function(event) {
        var styleUrl = '/static/vendor/bower_components/styles/' + event.val + '.csl';
        $.get(styleUrl).done(function(style) {
            self.updateStyle(style);
        }).fail(function(jqxhr, status, error) {
            console.log('Failed to load style');
        });
    });
};

CitationGrid.prototype.updateStyle = function(style) {
    this.style = style;
    this.bibliographies = {};
    this.treebeard.tbController.redraw();
};

CitationGrid.prototype.makeBibliography = function(folder) {
    var data = objectify(
        folder.children.filter(function(child) {
            return child.kind === 'item';
        }).map(function(child) {
            return child.data.csl;
        })
    );
    var citeproc = citations.makeCiteproc(this.style, data, 'text');
    var bibliography = citeproc.makeBibliography();
    if (bibliography[0].entry_ids) {
        return utils.reduce(
            utils.zip(bibliography[0].entry_ids, bibliography[1]), {},
            function(pair, acc) {
                return acc[pair[0][0]] = pair[1];
            }
        );
    }
    return {};
};

CitationGrid.prototype.getBibliography = function(folder) {
    this.bibliographies[folder.id] = this.bibliographies[folder.id] || this.makeBibliography(folder);
    return this.bibliographies[folder.id];
};

CitationGrid.prototype.resolveRowAux = function(item) {
    var self = this;
    return [{
        data: 'csl',
        folderIcons: true,
        custom: function(item) {
            if (item.kind === 'folder') {
                return item.data.name;
            } else {
                var bibliography = self.getBibliography(item.parent());
                return bibliography[item.data.csl.id];
            }
        }
    }, {
        // Wrap callback in closure to preserve intended `this`
        custom: function() {
            return renderActions.apply(self, arguments);
        }
    }];
};

module.exports = CitationGrid;
