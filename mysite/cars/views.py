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

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServiceTaskViewSet(viewsets.ModelViewSet):
    queryset = ServiceTask.objects.all()
    serializer_class = ServiceTaskSerializer

def index(request):
    return render(request, 'cars/index.html', dict(schedule=False))

def setup(request):
    import setup_db
    return HttpResponse(setup_db.setup())

def schedule(request):

    def _all(dbmodel):
        return dbmodel.objects.all()

    def _datetime(datetime):
        return str(datetime) if datetime else ''

    def _dict(data, fn):
        return dict([ (each.id, dict(id=each.id, full=str(each), **fn(each)))
            for each in data ])

    data = dict(
        owners = _dict(_all(Owner), lambda owner: dict(
            name = owner.name,
        )),
        tasks = _dict(_all(Task), lambda task: dict(
            name = task.name,
            engines = [ engine.id for engine in task.engines.all() ],
        )),
        makes = _dict(_all(Make), lambda make: dict(
            name = make.name,
            models = _dict(make.model_set.all(), lambda model: dict(
                name = model.name,
            )),
        )),
        models = _dict(_all(Model), lambda model: dict(
            name = model.name,
            engine = model.engine.id,
            engine_name = model.engine.name,
        )),
        cars = _dict(_all(Car), lambda car: dict(
            owner = car.owner.id,
            owner_name = car.owner.name,
            make = car.model.make.id,
            make_name = car.model.make.name,
            model = car.model.id,
            model_name = car.model.name,
            engine = car.model.engine.id,
            engine_name = car.model.engine.name,
            year = car.year,
            plate = car.plate,
            services = [ each.id for each in car.service_set.all() ],
        )),
        services = _dict(_all(Service), lambda service: dict(
            car = service.car.id,
            car_name = str(service.car),
            odometer = service.odometer,
            sched = _datetime(service.sched),
            enter = _datetime(service.enter),
            exit = _datetime(service.exit),
            total = str(service.total),
            observations = service.observations,
            servicetasks = _dict(service.servicetask_set.all(), lambda servicetask: dict(
                task = servicetask.task.id,
                task_name = servicetask.task.name,
            )),
        )),
    )

    # print 'data', data
    return render(request, 'cars/schedule.html', dict(schedule=True, data=json.dumps(data)))

def ajax(request):
    print 'ajax', request.POST
    return HttpResponse({})

