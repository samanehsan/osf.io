<%inherit file="base.mako"/>

<%def name="title()">Dropbox Addon</%def>

<%def name="content()">
    <h3>
##    <img src="${icon_url}">
    Dropbox
    <small><a class="pull-right" href="${node.web_url_for('node_setting')}">View all addons</a></small>
    </h3>
    <div class="col-md-6">
        <p>
            <a href ="https://www.dropbox.com/">Dropbox</a> is a popular online file storage program. After linking your OSF project to Dropbox, you can add
            files to your Dropbox folder and those files can be accessed via the OSF. Likewise, files added to the
            Dropbox folder in your OSF account will update your Dropbox account with that file.
        </p>
    <br/>
    <a class="btn btn-success" href=${node.web_url_for('addon_terms', provider='dropbox')}>Connect Account</a>
    </div>
    <div class="col-md-6">
    </div>
</%def>