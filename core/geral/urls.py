from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'ponto.views.home', name='home'),
    url(r'^relatorio/(?P<id_inicio>[0-9]+)/(?P<id_fim>[0-9]+)$',
    	'ponto.views.relatorio', name='relatorio'),
    url(r'^registrar/(?P<momento>\w+)$',
        'ponto.views.registrar', name='registrar'),
    url(r'^ios_login/$',
        'ponto.views.ios_login', name='ios_login'),
    url(r'^ios_logout/$',
        'ponto.views.ios_logout', name='ios_logout'),
    url(r'^ios_home/$',
        'ponto.views.ios_home', name='ios_home'),
    url(r'^ios_relatorio/$',
        'ponto.views.ios_relatorio', name='ios_relatorio'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
)

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += patterns('django.views.static',
                            (r'media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT,
                                                              'show_indexes': True}),)