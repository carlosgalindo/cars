from django.conf.urls import patterns, url
from cars import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    # url(r'^setup_db$', views.setup_db, name='setup_db'),
)
