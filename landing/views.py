from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import datetime

# from .forms import ScheduleClassForm

def index(request):
    if not request.user.is_authenticated:
        return redirect('loginPage')

    today = datetime.datetime.utcnow()
    upcoming = ''

    context = {
        'today': today,
        'upcoming': upcoming
    }
    return render(request, 'landing/index.html', context)


@login_required
def schedule(request):
    # form = ScheduleClassForm()
    context = {}
    return render(request, 'landing/schedule.html', context)
