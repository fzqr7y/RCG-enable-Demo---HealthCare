from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.big_data, name='home'),
    url(r'^rcg/$', views.rcg, name='rcg'),
    url(r'^members/$', views.members, name='members'),
    url(r'^providers/$', views.providers, name='providers'),
    url(r'^member/(?P<pk>\d+)/$', views.member_detail, name='member_detail'),
    url(r'^membertest/(?P<pk>\d+)/$', views.member_detail1, name='member_detail1'),
    url(r'^sms/receive/$', views.receive_sms, name='receive_sms'),
    url(r'^sms2/$', views.sms2, name='sms2'),
    url(r'^sms/(?P<pk>\d+)/$', views.sms, name='sms'),
    url(r'^heartrate2/(?P<pk>\d+)/$', views.heartrate2, name='heartrate2'),
    url(r'^map_county/(?P<pk>\d+)/$', views.map_county, name='map_county'),
    url(r'^provider_members/(?P<pk>\d+)/$', views.provider_members, name='provider_members'),
    url(r'^county_lookup/$', views.county_lookup, name='county_lookup'),

    # http://stackoverflow.com/questions/5871730/need-a-minimal-django-file-upload-example
    # url(r'^user_profile_upload/$', views.user_profile_upload,
    #     name='user_profile_upload'),

    url(r'^posts2/new/$', views.post_ajax_create, name='post_ajax_create'),
    url(r'^posts2/$', views.post_ajax, name='post_ajax'),
    url(r'^posts$', views.post_list, name='post_list'),
    url(r'^drafts$', views.post_draft_list, name='post_draft_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail,
        name='blog.views.post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>\d+)/publish/$', views.post_publish,
        name='post_publish'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post,
        name='add_comment_to_post'),
    url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve,
        name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove,
        name='comment_remove'),
]