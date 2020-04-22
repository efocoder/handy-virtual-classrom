import uuid

from django.db import models
from accounts.models import MyUser


class ScheduleClass(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    scheduled_by = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    start_date = models.DateField(null=False)
    time_start = models.TimeField(null=False)
    time_end = models.TimeField(null=False)
    # class_id = models.CharField(max_length=9, null=False)
    schedule_title = models.CharField(max_length=50, null=False)
    status = models.BooleanField(default=False, verbose_name='open or closed status')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'scheduled_classes'

    def __str__(self):
        return self.schedule_title


class ClassRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    schedule_id = models.ForeignKey(ScheduleClass, on_delete=models.CASCADE)
    class_unique_name = models.CharField(max_length=100)
    extrid = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'class_rooms'


    def __str__(self):
        return  self.class_unique_name


class InvitedList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    schedule_id = models.ForeignKey(ScheduleClass, on_delete=models.CASCADE)
    # class_name = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    invited_user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    twilio_sid = models.CharField(max_length=100, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'invited_lists'

    # def __str__(self):
    #     return self.schedule_id