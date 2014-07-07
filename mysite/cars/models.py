from django.db import models

class NameModel(models.Model):
    "Abstract model with name field."
    name = models.CharField('Name', max_length=200, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True

class Owner(NameModel):
    pass

class Make(NameModel):
    pass

class Model(NameModel):
    make = models.ForeignKey(Make)

class Task(NameModel):
    pass

class Engine(NameModel):
    no_tasks = models.ForeignKey(Task)
