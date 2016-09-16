from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home, name='index'),
    url(r'^heartrate/get/$', views.get_heartrate, name='get_heartrate'),
    url(r'^callback/$', views.callback, name='callback'),
    url(r'^get_access/$', views.get_access, name='get_access'),
    url(r'^get_data/$', views.get_data, name='get_data'),
]
