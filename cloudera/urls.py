from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home, name='index'),
    url(r'^impyla/$', views.impyla, name='impyla'),
    url(r'^heartrate/get/$', views.get_heartrate, name='get_heartrate'),
    url(r'^heartrate2/get/$', views.get_heartrate2, name='get_heartrate2'),
    url(r'^pg_heartrate/get/$',
        views.get_pg_heartrate, name='get_pg_heartrate'),
]
