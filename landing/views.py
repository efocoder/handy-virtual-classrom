from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
import datetime
import time
import calendar

from accounts.models import MyUser
from .forms import ScheduleClassForm
from .models import ScheduleClass, ClassRoom, InvitedList

from twilio_details import twilio


@login_required
def index(request):
    today = datetime.datetime.now()
    upcoming = InvitedList.objects.filter(invited_user_id__exact=request.user.pk) \
        .select_related().values('twilio_sid',
                                 'schedule_id',
                                 'schedule_id__schedule_title',
                                 'schedule_id__time_start',
                                 'schedule_id__start_date',
                                 'schedule_id__scheduled_by__username'
                                 ) \
        .filter(schedule_id__start_date__exact=today.date(), schedule_id__time_start__gt=today.time()) \
        .order_by('schedule_id__time_start')

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
            schedule.scheduled_by = MyUser.objects.get(pk=request.user.pk)
            schedule.status = calculate_date_difference(request.POST['start_date'], request.POST['time_start'],
                                                        request.POST['time_end'])
            schedule.save()

            class_room = create_classroom(request, schedule.pk)
            print(class_room)

            messages.success(request, 'Class schedules successfully')
            return redirect('landing')

    context = {'form': form}
    return render(request, 'landing/schedule.html', context)


@login_required
def connect(request):
    context = {}
    return render(request, 'landing/connect.html', context)


def session(request, class_unique_name):
    token = twilio.generate_access_token(request.user.pk, class_unique_name)

    return token


def callback(request):
    pass


def generate_class_unique_name():
    current_datetime = str(calendar.timegm(time.gmtime()))
    prefix = 'HVC'
    classroom_name = prefix + '-' + current_datetime
    check_id = ClassRoom.objects.filter(class_unique_name__exact=classroom_name)

    if check_id.exists():
        generate_class_unique_name()

    return classroom_name


def calculate_date_difference(start_date, start_time, end_time):
    status = False
    if start_date == datetime.datetime.utcnow() and (end_time - start_time == 0):
        status = True

    return status


def create_classroom(request, schedule_id):
    class_name = generate_class_unique_name()

    twilio_room = twilio.create_room(request, class_name)

    print(twilio_room)
    schedule = ScheduleClass.objects.get(pk=schedule_id)
    room = ClassRoom(schedule_id=schedule, class_unique_name=class_name, extrid=twilio_room.sid)
    room.save()

    invited_list_insert(twilio_room.sid, schedule_id, request)

    return room


def invited_list_insert(twilio_sid, schedule_id, request):
    schedule = ScheduleClass.objects.get(pk=schedule_id)
    invited_user = MyUser.objects.get(pk=request.user.pk)

    check = InvitedList.objects.filter(invited_user_id__exact=request.user.pk, schedule_id__exact=schedule_id)
    invite = None
    if check.exists():
        pass
    else:
        invite = InvitedList(schedule_id=schedule, invited_user_id=invited_user, twilio_sid=twilio_sid)
        invite.save()

    return invite
