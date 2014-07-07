from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class NameModel(models.Model):
    "Abstract model with name field."
    name = models.CharField('Name', max_length=200) # unique=True

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True

def _datetime():
    return models.DateTimeField(blank=True, null=True)

def _text():
    return models.TextField(blank=True)

class Owner(NameModel):
    pass

class Engine(NameModel):
    pass

class Make(NameModel):
    pass

class Model(NameModel):
    make = models.ForeignKey(Make)
    engine = models.ForeignKey(Engine)

    def __unicode__(self):
        return ', '.join(map(unicode, [ self.make, self.name, self.engine ]))

class Task(NameModel):
    engines = models.ManyToManyField(Engine)

    def engines_(self):
        return ', '.join([ engine.name for engine in self.engines.all() ])

class Car(models.Model):
    owner = models.ForeignKey(Owner)
    model = models.ForeignKey(Model)
    year = models.PositiveIntegerField(validators=[MinValueValidator(2000), MaxValueValidator(2015)])
    plate = models.CharField(max_length=8, blank=True)

    def __unicode__(self):
        return ', '.join([ unicode(each) for each in [
            self.model,
            self.year,
            self.plate,
            self.owner,
        ] if each ])

    def make_(self): return self.model.make.name
    def model_(self): return self.model.name
    def engine_(self): return self.model.engine.name

class Service(models.Model):
    car = models.ForeignKey(Car)
    mileage = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(300000)])
    sched = _datetime()
    enter = _datetime()
    exit = _datetime()
    observations = _text()
    total = models.DecimalField(default=0, max_digits=7, decimal_places=2)

    def __unicode__(self):
        return '%s ; mileage: %s' % (self.car, self.mileage)

    def owner_(self): return self.car.owner
    def make_(self): return self.car.make_()
    def model_(self): return self.car.model_()
    def engine_(self): return self.car.engine_()
    def year_(self): return self.car.year
    def plate_(self): return self.car.plate
    def sched_(self): return self.sched or ''
    def enter_(self): return self.enter or ''
    def exit_(self): return self.exit or ''

class ServiceTask(models.Model):
    service = models.ForeignKey(Service)
    task = models.ForeignKey(Task)
    start = _datetime()
    end = _datetime()
    observations = _text()

    def owner_(self): return self.service.owner_()
    def make_(self): return self.service.make_()
    def model_(self): return self.service.model_()
    def year_(self): return self.service.year_()
    def engine_(self): return self.service.engine_()
    def start_(self): return self.start or ''
    def end_(self): return self.end or ''

    def __unicode__(self):
        return '%s @ %s' % (self.task, self.service.car)
