from django.forms import ModelForm, TextInput, DateInput, TimeInput
from .models import ScheduleClass, ClassRoom


class ScheduleClassForm(ModelForm):

    class Meta:
        model = ScheduleClass
        fields = ['schedule_title', 'start_date', 'time_start', 'time_end']
        widgets = {
            'start_date': DateInput(attrs={'class':'start_date'}),
            'time_start': TimeInput(attrs={'class':'time_start'}),
            'time_end': TimeInput(attrs={'class':'time_end'}),
        }
