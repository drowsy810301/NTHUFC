from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^$', views.users, name='profile'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^delete_photo/(?P<delete_id>.*)/$', views.delete_photo),
    url(r'^locked/$', views.locked_out, name='locked_out'),
    url(r'^forget_password/$', views.forget_password, name='forget_password'),
    url(r'^forget_password_confirm/(?P<activation_key>\w+)/', views.forget_password_confirm, name='forget_password_confirm'),
)
