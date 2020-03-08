from django.contrib import admin
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index.as_view(), name='index'),
    url(r'^eventlist/$', views.eventlist),
    url(r'^event/$', views.event),
    url(r'^register/$', views.register),
    url(r'^login/$', views.login),
    url(r'^registerevent/$', views.registerevent),
    url(r'^store/$', views.store),
    url(r'^auth/$', views.auth_view),
    url(r'^storepart/$', views.storepart)
]