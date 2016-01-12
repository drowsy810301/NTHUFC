from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    #url(r'^$', views.photos, name='photos'),
    #uncomment the following line for upload testing
    #url(r'^upload/(?P<photo_id>[0-9]+)/', views.upload, name='upload'),
    url(r'^$',views.show, name='photos'),
    url(r'^ajax_post_comment/', views.ajax_post_comment, name='ajax_post_comment'),
    url(r'^ajax_post_like/', views.ajax_post_like, name='ajax_post_like'),
    url(r'^ajax_get_votes/', views.ajax_get_votes, name='ajax_get_votes'),
    url(r'^vote/', views.vote, name='vote'),
    url(r'^test/', views.test, name='test'),
)
