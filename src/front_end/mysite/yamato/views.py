from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    context = {}
    time_matrix = [[[0]*20, [1]*20, [4]*20, [9]*20],
               [[1]*20, [0]*20, [1]*20, [4]*20],
               [[4]*20, [1]*20, [0]*20, [1]*20],
               [[9]*20, [4]*20, [1]*20, [0]*20]]
    if request.method == 'POST':
        context["currentTime"] = request.POST["currentTime"]
        return render(request, 'yamato/index.html', context)
    return render(request, 'yamato/index.html', context)