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
        fields = ('url', 'name')

class EngineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Engine
        fields = ('url', 'name')
