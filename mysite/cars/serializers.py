from rest_framework import serializers
from cars.models import *

class OwnerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Owner
        fields = ('url', 'name')

class MakeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Make
        fields = ('url', 'name')

class ModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Model
        fields = ('url', 'name', 'make', 'engine')

class EngineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Engine
        fields = ('url', 'name')

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ('url', 'name')

class CarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Car
        fields = ('url', 'owner', 'model', 'year', 'plate')

class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Service
        fields = ('url', 'car', 'odometer', 'sched', 'enter', 'exit', 'total', 'observations')

class ServiceTaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ServiceTask
        fields = ('url', 'service', 'task', 'start', 'end', 'observations')
