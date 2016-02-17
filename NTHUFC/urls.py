from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'NTHUFC.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('index.urls', namespace='index')),
    url(r'^photos/', include('photos.urls', namespace='photos')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^marker/', include('locationMarker.urls', namespace='locationMarker')),
)#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''
if settings.DEBUG == False:
    urlpatterns += patterns('',
        url(r'^media/uploads/mages/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT+'uploads/images/',
        }),
		url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
)
'''

