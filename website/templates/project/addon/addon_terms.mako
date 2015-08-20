<%inherit file="base.mako"/>

<%def name="content()">
    <div class="col-md-12 addonTerms">
    ${addon_capabilities}
    <br/>
    <div class="pull-right">
        <button class="btn btn-default">Cancel</button>
        <a data-bind="click: connectAccount" class="btn btn-success connect-account">Accept</a>
    </div>
    </div>
</%def>

<%def name="javascript_bottom()">
    <% import json %>
    <script>
        window.contextVars = $.extend(true, {}, window.contextVars, {
            currentUser: {
                hasAuth: ${json.dumps(user_has_auth)}
            }
        })
    </script>

    <script src=${"/static/public/js/addon-terms.js" | webpack_asset}></script>

</%def>