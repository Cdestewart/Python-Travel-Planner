from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.new),
    url(r'^login$', views.login),
    url(r'travels$', views.dashboard),
    url(r'addtrip$', views.addpage),
    url(r'add$', views.addtrip),
    url(r'view/(?P<num>\d+)$', views.details),
    url(r'subscribe/(?P<num>\d+)$', views.subscribe),
    url(r'delete/(?P<num>\d+)$', views.delete),
    url(r'unsubscript/(?P<num>\d+)$', views.cancel),
    url(r'^logoff$', views.logout)
]