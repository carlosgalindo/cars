from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    makes = Make.objects.all()
    # return HttpResponse(', '.join([ each.name for each in makes ]))
    return render(request, 'cars/index.html', dict())

def setup(request):
    import setup_db
    return HttpResponse(setup_db.setup())
