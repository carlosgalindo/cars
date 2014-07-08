from django.shortcuts import render
from django.http import HttpResponse

from cars.models import *
import json

from rest_framework import viewsets
from cars.serializers import *

class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

class MakeViewSet(viewsets.ModelViewSet):
    queryset = Make.objects.all()
    serializer_class = MakeSerializer

class ModelViewSet(viewsets.ModelViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer

class EngineViewSet(viewsets.ModelViewSet):
    queryset = Engine.objects.all()
    serializer_class = EngineSerializer

def index(request):
    return render(request, 'cars/index.html', dict(data={}))

def setup(request):
    import setup_db
    return HttpResponse(setup_db.setup())

def schedule(request):

    def _all(dbmodel):
        return dbmodel.objects.all()

    def _dict(data, fn):
        return dict([ (each.id, dict(id=each.id, **fn(each)))
            for each in data ])

    def _models(make):
        return _dict(make.model_set.all(), lambda model: dict(name=model.name))

    data = dict(
        makes = _dict(_all(Make), lambda make: dict(name=make.name, models=_models(make))),
        cars = _dict(_all(Car), lambda car: dict(
            owner = car.owner.name,
            make = car.model.make.name,
            model = car.model.name,
            engine = car.model.engine.name,
            year = car.year,
            plate = car.plate,
        )),
    )

    print 'data', data
    return render(request, 'cars/schedule.html', dict(data=json.dumps(data)))
