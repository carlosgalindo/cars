
def db_models():
    from django.db.models import get_app, get_models
    app = get_app('cars')
    models = get_models(app)
    # print 'utils.models', app, models
    return models

def db_truncate(dbmodel):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute('TRUNCATE TABLE "%s"' % dbmodel.__name__)
