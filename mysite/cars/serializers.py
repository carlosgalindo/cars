from rest_framework import serializers
from cars.models import *

class OwnerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Owner
        fields = ('url', 'id', 'name')

class MakeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Make
        fields = ('url', 'id', 'name')

class ModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Model
        fields = ('url', 'id', 'name', 'make', 'engine')

class EngineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Engine
        fields = ('url', 'id', 'name')

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ('url', 'id', 'name')

class CarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Car
        fields = ('url', 'id', 'owner', 'model', 'year', 'plate')

class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Service
        fields = ('url', 'id', 'car', 'odometer', 'sched', 'enter', 'exit', 'total', 'observations')

class ServiceTaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ServiceTask
        fields = ('url', 'id', 'service', 'task', 'start', 'end', 'observations')
