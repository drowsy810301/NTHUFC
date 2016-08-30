from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^ajax_post_comment/', views.ajax_post_comment, name='ajax_post_comment'),
    url(r'^ajax_post_like/', views.ajax_post_like, name='ajax_post_like'),
    url(r'^ajax_get_votes/', views.ajax_get_votes, name='ajax_get_votes'),
    url(r'^ajax_get_photo_details/', views.ajax_get_photo_details, name='ajax_get_photo_details'),
    url(r'^vote/$', views.vote, name='vote'),
    url(r'^vote/(?P<page>[0-9]+)$', views.vote, name='vote_with_page'),
    url(r'^flickr_authorization_redirect/(?P<flickr_photo_id>[0-9]+)/(?P<facebook_post_id>[_0-9]+)/', views.flickr_authorization_redirect, name='flickr_authorization_redirect'),
    url(r'^ajax_post_flickr_favorite/', views.ajax_post_flickr_favorite, name='ajax_post_flickr_favorite'),
    url(r'^ajax_report_comment/', views.ajax_report_comment, name='ajax_report_comment'),
    url(r'^sorted_judge/$', views.sorted_judge, name='judge'),
    url(r'^sorted_judge/(?P<page>[0-9]+)$', views.sorted_judge, name='sorted_judge_with_page'),
    url(r'^judge/$', views.judge, name='judge'),
    url(r'^judge/(?P<page>[0-9]+)$', views.judge, name='judge_with_page'),
	url(r'^select/$', views.select, name='select'),
	url(r'^select1/$', views.select1, name='select1'),
	url(r'^select2/$', views.select2, name='select2'),
	url(r'^select3/$', views.select3, name='select3'),
	url(r'^select4/$', views.select4, name='select4'),
	url(r'^printall/$', views.printall, name='printall'),
)
