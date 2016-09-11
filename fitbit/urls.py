from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home, name='index'),
    url(r'^heartrate/get/$', views.get_heartrate, name='get_heartrate'),
]
