<%inherit file="project/project_base.mako"/>

<%def name="title()">${node['title']} Discussions</%def>

% if user['can_comment'] or node['has_comments']:
    <%include file="include/comment_template.mako"/>
% endif

<div class="row">
    <div id="discussions">
        <div class="col-sm-3 affix-parent">
            <div class="panel panel-default osf-affix" data-spy="affix" data-offset-top="70" data-offset-bottom="263">
                <ul class="nav nav-stacked nav-pills">
                    <!-- total -->
                    <li data-bind="css: { active: filter() == 'total'}, click: function() { setFilter('total') }">
                        <a>All Comments</a>
                    </li>

                    <!-- project overview -->
                    <li data-bind="css: { active: filter() == 'node'}, click: function() { setFilter('node') }">
                        <a>Project Overview</a>
                    </li>

                    <!-- wiki -->
                    % if addons:
                        % if 'wiki' in addons_enabled:
                            <li data-bind="css: { active: filter() == 'wiki'},  click: function() { setFilter('wiki') }">
                                <a>Wiki</a>
                            </li>
                        % endif
                    % endif

                    <!-- files -->
                    <li data-bind="css: { active: filter() == 'files'}, click: function() { setFilter('files') }">
                        <a>Files</a>
                    </li>
                </ul>
            </div>
        </div>

        <div class="col-sm-9">
            <h3 data-bind="text:pageTitle"></h3>
            <div data-bind="template: {name: 'commentTemplate', foreach: filterComments}"></div>
            <div data-bind="if: filterComments().length == 0">
                <div data-bind="if: filter() == 'total'">
                    There are no comments on this project yet. Go to the
                    <a href="${node['url']}">project overview page</a> and open the comment pane to make a comment.
                </div>
                <div data-bind="if: filter() == 'node'">
                    There are no comments on the project overview page yet. Go to the
                    <a href="${node['url']}">project overview page</a> and open the comment pane to make a comment.
                </div>
                <div data-bind="if: filter() == 'wiki'">
                    There are no comments on the {{ filter }} page yet. Go to the
                    <a href="${node['url']}{{ filter }}">{{ filter }} page</a>, and open the comment pane to make a comment.
                </div>
                <div data-bind="if: filter() == 'files'">
                    There are no comments on the {{ filter }} page yet. Go to the
                    <a href="${node['url']}{{ filter }}">{{ filter }} page</a>, view a file and open the comment pane to make a comment.
                </div>
            </div>
        </div>
    </div>
</div>

<%def name="stylesheets()">
    ${parent.stylesheets()}

    <link rel="stylesheet" href="/static/css/pages/project-page.css">
</%def>

<%def name="javascript_bottom()">
<% import json %>
${parent.javascript_bottom()}

<script src=${"/static/public/js/discussions-page.js" | webpack_asset}></script>
</%def>
