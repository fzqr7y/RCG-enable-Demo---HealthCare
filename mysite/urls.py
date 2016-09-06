"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# from django.conf.urls import url
from django.conf.urls import include, url
from django.contrib import admin
import django.contrib.auth.views

# https://github.com/axelpale/minimal-django-file-upload-example/blob/master/src/for_django_1-9/myproject/myproject/urls.py
# from django.conf import settings
# from django.conf.urls.static import static
# from django.views.generic import RedirectView
# urlpatterns = [
#     url(r'^admin/', include(admin.site.urls)),
#     url(r'^myapp/', include('myproject.myapp.urls')),
#     url(r'^$', RedirectView.as_view(url='/myapp/list/', permanent=True)),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', django.contrib.auth.views.login, name='login'),
    url(r'^accounts/logout/$', django.contrib.auth.views.logout,
        name='logout', kwargs={'next_page': '/'}),
    # url(r'', include('blog.urls')),
    url(r'', include('demo.urls')),
    # url(r'^userprofile$', RedirectView.as_view(
    #     url='/user_profile_upload/', permanent=True)),
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
