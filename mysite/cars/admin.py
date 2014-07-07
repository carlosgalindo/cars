from django.contrib import admin
from django.contrib.auth.models import User, Group

import utils
dbmodels = utils.db_models()

for dbmodel in [ User, Group ]:
    admin.site.unregister(dbmodel)

# Fields, Sets, Orders ... https://docs.djangoproject.com/en/1.6/intro/tutorial02/#customize-the-admin-form

for dbmodel in dbmodels:
    admin.site.register(dbmodel)
