from django.shortcuts import render
from django.http import HttpResponse
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError

from decimal import Decimal

from cars.models import *
import json

import utils

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

def _data(config=None):
    # print '_data', config
    def _all(dbmodel):
        return dbmodel.objects.all()
    def _list(dbmodel):
        return [ config.get(dbmodel) ] if config else _all(dbmodel)
    def _datetime(datetime):
        return str(datetime) if datetime else ''
    def _dict(data, fn):
        return dict([ (each.id, dict(id=each.id, full=str(each), **fn(each)))
            for each in data ])
    data = dict(
        owners = _dict(_list(Owner), lambda owner: dict(
            name = owner.name,
        )),
        cars = _dict(_list(Car), lambda car: dict(
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
        services = _dict(_list(Service), lambda service: dict(
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
                start = _datetime(servicetask.start),
                end = _datetime(servicetask.end),
                observations = servicetask.observations,
            )),
        )),
    )
    if not config:
        data.update(
            tasks = _dict(_all(Task), lambda task: dict(
                name = task.name,
                engines = [ engine.id for engine in task.engines.all() ],
            )),
            models = _dict(_all(Model), lambda model: dict(
                name = model.name,
                engine = model.engine.id,
                engine_name = model.engine.name,
            )),
        )
    # print '_data', data
    return data

def schedule(request):
    data = _data()
    return render(request, 'cars/schedule.html', dict(schedule=True, data=json.dumps(data)))

def ajax(request):
    pvars = json.loads(request.POST.get('data'), parse_float=Decimal)
    # print 'ajax', pvars
    def _get(key, default=None):
        pv = pvars.get(key)
        # print '_get', key, pv
        return pv or ('' if default is None else default)
    def _ref(key, dbmodel):
        pv = _get(key)
        pv = dbmodel.objects.get(pk=pv) if pv else None
        # print 'ajax > _ref', key, dbmodel, pv.id if pv else None, pv
        return pv
    def _get_datetime(key):
        return _get(key) or None
    def _new(dbmodel, **kwargs):
        return dbmodel.objects.create(**kwargs)
    def _int(string):
        try: v = int(string)
        except: v = None
        return v
    def _decimal(string):
        try: v = Decimal(string)
        except: v = None
        return v
    service = _ref('ref_service', Service)
    car = _ref('ref_car', Car)
    owner = _ref('ref_owner', Owner)
    # print 'ajax > refs', [ service, car, owner ]
    errors = []
    try:
        with transaction.atomic():
            if service:
                car = service.car
            if car:
                owner = car.owner
            else:
                if not owner:
                    owner = _new(Owner, name=_get('car_owner_name'))
                model = _ref('car_model', Model)
                car = _new(Car,
                    owner = owner,
                    model = model,
                    year = _int(_get('car_year')) or 2000,
                    plate = _get('car_plate'),
                )
            if not service:
                dbvars = dict(
                    car = car,
                    odometer = _int(_get('odometer')) or 0,
                    sched = _get_datetime('sched'),
                    enter = _get_datetime('enter'),
                    exit = _get_datetime('exit'),
                    total = _decimal(_get('total')) or 0,
                    observations = _get('observations'),
                )
                service = _new(Service, **dbvars)
            # print 'car', car
            # print 'service', service
            webtasks = pvars.get('servicetasks') or []
            # print 'webtasks', webtasks
            for webtask in webtasks:
                pvars = webtask # reset to reuse _get methods above.
                servicetask_id = _int(webtask.get('id'))
                # print 'servicetask_id', servicetask_id
                task_id = _int(webtask.get('task'))
                task = Task.objects.get(pk=task_id) if task_id else None
                # print 'task', task
                if task:
                    dbvars = dict(
                        start = _get_datetime('start'),
                        end = _get_datetime('end'),
                        observations = _get('observations'),
                    )
                    # print 'dbvars', dbvars
                    if servicetask_id: # update.
                        # filter (instead of get) to use update.
                        ServiceTask.objects.filter(pk=servicetask_id).update(**dbvars)
                    else: # create.
                        dbvars.update(
                            service = service,
                            task = task,
                        )
                        err = utils.validate_engine(dbvars)
                        if err:
                            raise ValidationError(err)
                        _new(ServiceTask, **dbvars)
            # NO deletes for now.
    except IntegrityError as e:
        errors.append('Not unique / valid.')
        # raise(e)
    except ValidationError as e:
        # print 'ValidationError @ views.py', e
        errors.append('Validation error: %s' % e)
        # raise(e)
    data = dict(
        error = ', '.join(errors),
        data = dict() if errors else _data({ Owner: owner, Car: car, Service: service }),
    )
    # print 'ajax > data', data
    return HttpResponse(json.dumps(data))
