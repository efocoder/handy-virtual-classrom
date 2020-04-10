from django.shortcuts import render

from datetime import date


def index(request):
    current_year = date.today().year
    context= {
        'copyright': current_year
    }
    return render(request, 'home/index.html', context)
