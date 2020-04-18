from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import datetime
import time
import calendar

from .forms import ScheduleClassForm
from .models import ScheduleClass, ClassRoom, InvitedList


@login_required
def index(request):
    today = datetime.datetime.utcnow()
    upcoming = ''

    context = {
        'today': today,
        'upcoming': upcoming
    }
    return render(request, 'landing/index.html', context)


@login_required
def schedule(request):
    print(request.user.pk)

    form = ScheduleClassForm()

    if request.method == 'POST':
        form = ScheduleClassForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.schedule_by = request.user.pk
            # schedule.class_id = generate_class_id()
            schedule.status = calculate_date_difference(request.POST['start_date'], request.POST['time_start'],
                                                        request.POST['time_end'])
            schedule.save()

            class_room = ClassRoom(schedule_id=schedule.pk, class_unique_name=generate_class_id())

            messages.success(request, 'Class schedules successfully')
            return redirect('landing')

    context = {'form': form}
    return render(request, 'landing/schedule.html', context)


def generate_class_id():
    current_datetime = str(calendar.timegm(time.gmtime()))
    prefix = 'HVC'
    class_id = prefix + '-' + current_datetime
    check_id = ScheduleClass.objects.filter(class_id__exact=class_id)

    if check_id.exists():
        generate_class_id()

    return class_id


def calculate_date_difference(start_date, start_time, end_time):
    status = False
    if start_date == datetime.datetime.utcnow() and (end_time - start_time == 0):
        status = True

    return status
