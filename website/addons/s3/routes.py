from framework.routing import Rule, json_renderer

from website.addons.s3 import views


settings_routes = {
    'rules': [
        Rule(
            [
                '/project/<pid>/s3/newbucket/',
                '/project/<pid>/node/<nid>/s3/newbucket/',
            ],
            'post',
            views.crud.create_new_bucket,
            json_renderer
        ),
        Rule(
            '/settings/s3/',
            'post',
            views.config.s3_authorize_user,
            json_renderer
        ),
        Rule(
            [
                '/project/<pid>/s3/settings/',
                '/project/<pid>/node/<nid>/s3/settings/',
            ],
            'post',
            views.config.s3_node_settings,
            json_renderer,
        ),
        Rule(
            [
                '/project/<pid>/s3/settings/',
                '/project/<pid>/node/<nid>/s3/settings/',
                '/project/<pid>/s3/config/',
                '/project/<pid>/node/<nid>/s3/config/',
            ],
            'delete',
            views.config.s3_remove_node_settings,
            json_renderer,
        ),
        Rule(
            [
                '/project/<pid>/s3/import-auth/',
                '/project/<pid>/node/<nid>/s3/import-auth/',
            ],
            'post',
            views.config.s3_node_import_auth,
            json_renderer,
        ),
        Rule(
            [
                '/project/<pid>/s3/authorize/',
                '/project/<pid>/node/<nid>/s3/authorize/',
            ],
            'post',
            views.config.s3_authorize_node,
            json_renderer,
        ),
        Rule(
            '/settings/s3/',
            'delete',
            views.config.s3_remove_user_settings,
            json_renderer,
        ),
    ],
    'prefix': '/api/v1',
}

api_routes = {
    'rules': [
        Rule(
            [
                '/project/<pid>/s3/hgrid/',
                '/project/<pid>/node/<nid>/s3/hgrid/',
                '/project/<pid>/s3/hgrid/<path:path>/',
                '/project/<pid>/node/<nid>/s3/hgrid/<path:path>/',
            ],
            'get',
            views.hgrid.s3_hgrid_data_contents,
            json_renderer
        ),
        Rule(
            [
                '/project/<pid>/s3/hgrid/dummy/',
                '/project/<pid>/node/<nid>/s3/hgrid/dummy/',
            ],
            'get',
            views.hgrid.s3_dummy_folder,
            json_renderer,
        ),
    ],
    'prefix': '/api/v1',
}


nonapi_routes = {
    'rules': []
}
