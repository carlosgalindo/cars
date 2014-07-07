from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class NameModel(models.Model):
    "Abstract model with name field."
    name = models.CharField('Name', max_length=200) # unique=True

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True

class Owner(NameModel):
    pass

class Engine(NameModel):
    pass

class Make(NameModel):
    pass

class Model(NameModel):
    make = models.ForeignKey(Make)
    engine = models.ForeignKey(Engine)

class Task(NameModel):
    non_engines = models.ManyToManyField(Engine)

class Car(models.Model):
    owner = models.ForeignKey(Owner)
    model = models.ForeignKey(Model)
    year = models.PositiveIntegerField(validators=[MinValueValidator(2000), MaxValueValidator(2015)])
    plate = models.CharField(max_length=8)

    def __unicode__(self):
        return 'PENDING Car'

class Service(models.Model):
    car = models.ForeignKey(Car)
    mileage = models.PositiveIntegerField(validators=[MaxValueValidator(300000)])
    sched = models.DateTimeField()
    enter = models.DateTimeField()
    exit = models.DateTimeField()
    observations = models.TextField()
    total = models.DecimalField(max_digits=7, decimal_places=2)

    def __unicode__(self):
        return 'PENDING Service'

class ServiceTask(models.Model):
    service = models.ForeignKey(Service)
    task = models.ForeignKey(Task)
    start = models.DateTimeField()
    end = models.DateTimeField()
    observations = models.TextField()

    def __unicode__(self):
        return 'PENDING ServiceTask'
