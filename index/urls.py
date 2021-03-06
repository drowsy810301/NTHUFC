from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^participate/$', views.participate, name='participate'),
    url(r'^q_a/$', views.q_a, name='q_a'),
    url(r'^poster/$', views.poster, name='poster'),
    url(r'^privacypolicy/$', views.privacypolicy, name='privacypolicy'),
    url(r'^map/$', views.map, name='map'),
)
