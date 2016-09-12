from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^members/$', views.members, name='members'),
    url(r'^providers/$', views.providers, name='providers'),
    url(r'^member/(?P<pk>\d+)/$', views.member_detail, name='member_detail'),
    # url(r'^member1$', views.member1_detail, name='member1_detail'),
    # url(r'^provider/(?P<pk>\d+)/edit/$', views.provider_edit, name='provider_edit'),
    url(r'^sms/receive/$', views.receive_sms, name='receive_sms'),
    url(r'^sms/$', views.sms, name='sms'),
    url(r'^heartrate/(?P<pk>\d+)/$', views.heartrate, name='heartrate'),
    url(r'^members2/$', views.members2, name='members2'),

    # http://stackoverflow.com/questions/5871730/need-a-minimal-django-file-upload-example
    # url(r'^user_profile_upload/$', views.user_profile_upload,
    #     name='user_profile_upload'),

    url(r'^posts2/new/$', views.post_ajax_create, name='post_ajax'),
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
