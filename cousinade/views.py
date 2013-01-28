# listing
# tree
# search
# edit
from django.shortcuts import render

from models import Person


def index(request):
    return render(request, 'index.html')

def listing(request):
    return render(request, 'listing.html', {'objects': Person.objects.all()})
