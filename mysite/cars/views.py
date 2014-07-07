from django.shortcuts import render
from django.http import HttpResponse

from cars.models import *

def index(request):
    makes = Make.objects.all()
    # return HttpResponse(', '.join([ each.name for each in makes ]))
    return render(request, 'cars/index.html', dict())
