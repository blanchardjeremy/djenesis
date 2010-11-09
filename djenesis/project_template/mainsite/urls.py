from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

handler500 = 'mainsite.views.error500'

urlpatterns = patterns('',

    (r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:
    # If we are in debug mode, prepend a rule to urlpatterns to serve the static media
    import re
    urlpatterns = patterns('',
        url(r'^robots.txt$', 'mainsite.views.robots_txt'),

        url(r'^%s/(?P<path>.*)$' % re.escape(settings.MEDIA_URL.strip('/')),
          'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    ) + urlpatterns
