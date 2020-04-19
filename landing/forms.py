import datetime
import time
import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django.forms import ModelForm, TextInput, DateInput, TimeInput
from .models import ScheduleClass, ClassRoom


class ScheduleClassForm(ModelForm):
    class Meta:
        model = ScheduleClass
        fields = ['schedule_title', 'start_date', 'time_start', 'time_end']
        widgets = {
            'start_date': DateInput(attrs={'class': 'start_date'}),
            'time_start': TimeInput(attrs={'class': 'time_start'}),
            'time_end': TimeInput(attrs={'class': 'time_end'}),
        }

    def clean_schedule_title(self, *args, **kwargs):
        schedule_title = self.cleaned_data.get('schedule_title')

        if not schedule_title:
            raise ValidationError(_('This field is required'))

        if not re.match("^[a-zA-Z0-9 ]*$", schedule_title):
            raise ValidationError(_('Letters and numbers only'))

        return schedule_title

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')

        if not start_date:
            raise ValidationError(_('This field is required'))

        if start_date < datetime.date.today():
            raise ValidationError(_('Invalid Date'))

        return start_date

    def clean_time_start(self):
        time_start = self.cleaned_data.get('time_start')

        if not time_start:
            raise ValidationError(_('This field is required'))

        if time_start <= datetime.datetime.now().time():
            raise ValidationError(_('Invalid time'))

        return time_start

    def clean_time_end(self):
        time_end = self.cleaned_data.get('time_end')
        time_start = self.clean_time_start()

        if not time_end:
            raise ValidationError(_('This field is required'))

        if time_start >= time_end:
            raise ValidationError(_('Start time cannot greater than or equal to end time'))

        return time_end
