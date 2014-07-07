
def db_models():
    from django.db.models import get_app, get_models
    app = get_app('cars')
    models = get_models(app)
    # print 'utils.models', app, models
    return models
