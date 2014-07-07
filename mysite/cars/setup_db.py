from cars.models import *

def _create(model, props):
    for each in props:
        name = each[0]
        if not model(name=name):
            model(name=name, **each[1] or dict()).save()

_create(Owner, [
    ('Steven Hines', None),
    ('Carlos Galindo', None),
    ('Vanessa Mar', None),
])

_create(Engine, [
    ('Electric', None),
    ('Gas', None),
    ('Diesel', None),
    ('Hybrid', None),
])

_create(Make, [
    ('Electric', None),
    ('Gas', None),
    ('Diesel', None),
    ('Hybrid', None),
])
