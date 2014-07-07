from django.contrib import admin
from django.contrib.auth.models import User, Group
from cars.models import *

for each in [ User, Group ]:
    admin.site.unregister(each)

# xAdmin = Fields, Sets, Orders ! ... https://docs.djangoproject.com/en/1.6/intro/tutorial02/#customize-the-admin-form

for each in [ Owner, Make, Model, Engine, Task ]:
    admin.site.register(each)
