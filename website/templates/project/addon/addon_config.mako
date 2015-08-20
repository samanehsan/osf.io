<%inherit file="project/project_base.mako"/>

<%def name="title()">${node['title']} Settings</%def>


    <h3>Connect Account</h3>
    <hr/>
    <div>
        % for node_settings_dict in addon_enabled_settings or []:
            ${render_node_settings(node_settings_dict)}
                % if not loop.last:
                    <hr />
                % endif
        % endfor
    </div>

<%def name="render_node_settings(data)">
    <%
       template_name = data['node_settings_template']
       tpl = data['template_lookup'].get_template(template_name).render(**data)
    %>
    ${tpl}
</%def>

<%def name="stylesheets()">
    ${parent.stylesheets()}

    <link rel="stylesheet" href="/static/css/pages/project-page.css">
</%def>

<%def name="javascript_bottom()">
    <% import json %>
    ${parent.javascript_bottom()}
    <script>
      window.contextVars = window.contextVars || {};
      window.contextVars.node = window.contextVars.node || {};
      window.contextVars.node.nodeType = '${node['node_type']}';
    </script>

    <script type="text/javascript" src=${"/static/public/js/project-settings-page.js" | webpack_asset}></script>

    % for js_asset in addon_js:
        <script src="${js_asset | webpack_asset}"></script>
    % endfor

</%def>