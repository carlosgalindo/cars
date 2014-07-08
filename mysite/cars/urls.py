from django.conf.urls import patterns, url
from cars import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^setup$', views.setup, name='setup'),
    url(r'^schedule$', views.schedule, name='schedule'),
)
