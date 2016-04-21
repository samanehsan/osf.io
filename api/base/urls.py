from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from settings import API_BASE

from . import views

base_pattern = '^{}'.format(API_BASE)

urlpatterns = [
    url(base_pattern,
        include(
            [
                url(r'^$', views.root, name='root'),
                url(r'^applications/', include('api.applications.urls', namespace='applications')),
                url(r'^comments/', include('api.comments.urls', namespace='comments')),
                url(r'^nodes/', include('api.nodes.urls', namespace='nodes')),
                url(r'^registrations/', include('api.registrations.urls', namespace='registrations')),
                url(r'^users/', include('api.users.urls', namespace='users')),
                url(r'^tokens/', include('api.tokens.urls', namespace='tokens')),
                url(r'^logs/', include('api.logs.urls', namespace='logs')),
                url(r'^files/', include('api.files.urls', namespace='files')),
                url(r'^docs/', include('rest_framework_swagger.urls')),
                url(r'^institutions/', include('api.institutions.urls', namespace='institutions')),
                url(r'^collections/', include('api.collections.urls', namespace='collections')),
                url(r'^guids/', include('api.guids.urls', namespace='guids'))
            ],
        )
        )
]


urlpatterns += static('/static/', document_root=settings.STATIC_ROOT)

handler404 = views.error_404
