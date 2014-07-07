from cars.models import *

import utils
dbmodels = utils.db_models()

def setup():
    if Engine.objects.first():
        return 'Canceled, already setup.'

    def _new(model, **kwargs):
        return model.objects.create(**kwargs)

    for name in [ 'Steven Hines', 'Carlos Galindo', 'Vanessa Mar' ]:
        _new(Owner, name=name)

    engines = dict([ (name, _new(Engine, name=name))
        for name in [ 'Diesel', 'Electric', 'Gas', 'Hybrid' ] ])
    print 'setup > engines', engines

    for name in [ 'Oil change', 'Tire rotation' ]:
        _new(Task, name=name)

    make = _new(Make, name='Dodge')
    for name in [ 'Dart', 'Avenger', 'Charger', 'Challenger' ]:
        _new(Model, name=name, make=make, engine=engines['Diesel'])

    return 'Done'
