from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    a = 123456789
    context = {'a': a}
    return render(request, 'yamato/index.html', context)