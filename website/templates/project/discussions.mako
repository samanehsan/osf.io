<%inherit file="project/project_base.mako"/>

<%def name="title()">${node['title']} Discussions</%def>

% if user['can_comment'] or node['has_comments']:
    <%include file="include/comment_template.mako"/>
% endif

<div class="row">
        <div class="col-sm-3 affix-parent">
            <div class="panel panel-default osf-affix" data-spy="affix" data-offset-top="70" data-offset-bottom="263">
                <ul class="nav nav-stacked nav-pills">
                    <!-- total -->
                    <li ${'class="active"' if page == 'total' else '' | n}>
                        <a href="${node['url'] + 'discussions/'}">All Comments</a>
                    </li>

                    <!-- project overview -->
                    <li ${'class="active"' if page == 'node' else '' | n}>
                        <a href="${node['url'] + 'discussions/?page=node'}">Project Overview</a>
                    </li>

                    <!-- wiki -->
                    % if addons:
                        % if 'wiki' in addons_enabled:
                            <li ${'class="active"' if page == 'wiki' else '' | n}>
                                <a href="${node['url'] + 'discussions/?page=wiki'}">Wiki</a>
                            </li>
                        % endif
                    % endif

                    <!-- files -->
                    <li ${'class="active"' if page == 'files' else '' | n}>
                        <a href="${node['url'] + 'discussions/?page=files'}">Files</a>
                    </li>
                </ul>
            </div>
        </div>

        <div class="col-sm-9">
            <div id="discussions" class="scripted">
                %if not page:
                    This is a single comment thread.
                %else:
                    <h3 data-bind="text:pageTitle"></h3>
                    <div data-bind="if: comments().length == 0 && !loadingComments()">
                        %if page == 'total':
                        <div>
                            There are no comments on this project yet. Go to the
                            <a href="${node['url']}">project overview page</a> and open the comment pane to make a comment.
                        </div>
                        %elif page == 'node':
                        <div>
                            There are no comments on the project overview page yet. Go to the
                            <a href="${node['url']}">project overview page</a> and open the comment pane to make a comment.
                        </div>
                        %elif page == 'wiki':
                        <div>
                            There are no comments on the wiki page yet. Go to the
                            <a href="${node['url'] + 'wiki/'}">wiki page</a>, and open the comment pane to make a comment.
                        </div>
                        %elif page == 'files':
                        <div>
                            There are no comments on the files page yet. Go to the
                            <a href="${node['url'] + '/files/'}">files page</a>, view a file and open the comment pane to make a comment.
                        </div>
                        %endif
                    </div>
                %endif
                <div data-bind="template: {name: 'commentTemplate', foreach: comments}"></div>
                <!-- ko if: loadingComments -->
                <div style="text-align: center;">
                    <div class="logo-spin logo-lg"></div>
                </div>
                <!-- /ko -->
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
<script>
    window.contextVars.comment = {};
    window.contextVars.comment.id = "${comment_id or ''}";
</script>
<script src=${"/static/public/js/discussions-page.js" | webpack_asset}></script>
</%def>
