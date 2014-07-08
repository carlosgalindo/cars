from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

def _name(**kwargs): return models.CharField('Name', max_length=200, unique=True, **kwargs)
def _datetime(*args, **kwargs): return models.DateTimeField(blank=True, null=True, *args, **kwargs)
def _text(**kwargs): return models.TextField('Observations', blank=True, **kwargs)

class Owner(models.Model):
    name = _name()

    def __unicode__(self):
        return self.name

class Engine(models.Model):
    name = _name()

    def __unicode__(self):
        return self.name

class Make(models.Model):
    name = _name()

    def __unicode__(self):
        return self.name

class Model(models.Model):
    name = _name()
    make = models.ForeignKey(Make, verbose_name='Make')
    engine = models.ForeignKey(Engine, verbose_name='Engine')

    def __unicode__(self):
        return ', '.join(map(unicode, [ self.make, self.name, self.engine ]))

class Task(models.Model):
    name = _name()
    engines = models.ManyToManyField(Engine, verbose_name='Engines')

    def __unicode__(self):
        return self.name

    def engines_(self): return ', '.join(sorted([ engine.name for engine in self.engines.all() ]))

class Car(models.Model):
    owner = models.ForeignKey(Owner, verbose_name='Owner')
    model = models.ForeignKey(Model, verbose_name='Model')
    year = models.PositiveIntegerField('Year', validators=[MinValueValidator(2000), MaxValueValidator(2015)])
    plate = models.CharField('Plate', max_length=8, blank=True)

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
    car = models.ForeignKey(Car, verbose_name='Car')
    odometer = models.PositiveIntegerField('Odometer', default=0, validators=[MaxValueValidator(300000)])
    sched = _datetime('Schedule')
    enter = _datetime('Enter / Arrival')
    exit = _datetime('Exit / Departure')
    total = models.DecimalField('Total', default=0, max_digits=7, decimal_places=2)
    observations = _text()

    def __unicode__(self):
        return '%s ; odometer: %s' % (self.car, self.odometer)

    def owner_(self): return self.car.owner
    def make_(self): return self.car.make_()
    def model_(self): return self.car.model_()
    def engine_(self): return self.car.engine_()
    def year_(self): return self.car.year
    def plate_(self): return self.car.plate
    def sched_(self): return self.sched or ''
    def enter_(self): return self.enter or ''
    def exit_(self): return self.exit or ''
    def tasks_(self): return ', '.join(sorted([ each.task.name for each in self.servicetask_set.all() ]))

class ServiceTask(models.Model):
    service = models.ForeignKey(Service, verbose_name='Service')
    task = models.ForeignKey(Task, verbose_name='Task')
    start = _datetime('Start')
    end = _datetime('End')
    observations = _text()

    def __unicode__(self):
        return '%s @ %s' % (self.task, self.service.car)

    def owner_(self): return self.service.owner_()
    def make_(self): return self.service.make_()
    def model_(self): return self.service.model_()
    def year_(self): return self.service.year_()
    def engine_(self): return self.service.engine_()
    def start_(self): return self.start or ''
    def end_(self): return self.end or ''
