from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',


    (r'^admin/', include(admin.site.urls)),
)


# Serve static media when DEBUG is on (development-use only).
if settings.DEBUG:
    import re
    
    urlpatterns = patterns('',
        url(r'^%s/(?P<path>.*)$' % re.escape(settings.MEDIA_URL.strip('/')), 
          'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )+urlpatterns
