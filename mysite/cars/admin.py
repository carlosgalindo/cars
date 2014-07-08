from django.contrib import admin
from django.contrib.auth.models import User, Group

from cars.models import *

import utils
dbmodels = utils.db_models()

for dbmodel in [ User, Group ]:
    admin.site.unregister(dbmodel)

class ModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'make', 'engine')

class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'engines_')

class CarAdmin(admin.ModelAdmin):
    list_display = ('owner', 'make_', 'model_', 'engine_', 'year', 'plate')

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('owner_', 'make_', 'model_', 'engine_', 'year_', 'plate_', 'odometer', 'sched_', 'enter_', 'exit_', 'tasks_', 'total')

class ServiceTaskAdmin(admin.ModelAdmin):
    list_display = ('owner_', 'make_', 'model_', 'year_', 'engine_', 'start_', 'end_')

dbadmins = [
    (Model, ModelAdmin),
    (Task, TaskAdmin),
    (Car, CarAdmin),
    (Service, ServiceAdmin),
    (ServiceTask, ServiceTaskAdmin),
]

for dbmodel, dbadmin in dbadmins:
    admin.site.register(dbmodel, dbadmin)
    dbmodels.remove(dbmodel)

for dbmodel in dbmodels:
    admin.site.register(dbmodel)
