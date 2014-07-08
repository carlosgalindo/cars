from django.conf.urls import patterns, url
from cars import views

from django.conf.urls import include
from rest_framework import routers
router = routers.DefaultRouter()
for er, eset in [
    (r'owners', views.OwnerViewSet),
    (r'makes', views.MakeViewSet),
    (r'models', views.ModelViewSet),
    (r'engines', views.EngineViewSet),
    (r'tasks', views.TaskViewSet),
    (r'cars', views.CarViewSet),
    (r'services', views.ServiceViewSet),
    (r'servicetasks', views.ServiceTaskViewSet),
]:
    router.register(er, eset)

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^setup$', views.setup, name='setup'),
    url(r'^schedule$', views.schedule, name='schedule'),

    url(r'^api/', include(router.urls)),
)
# print 'urlpatterns', urlpatterns
