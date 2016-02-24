from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^ajax_send_feedback/$', views.ajax_send_feedback, name='ajax_send_feedback'),
)
