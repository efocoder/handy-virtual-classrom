from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='landing'),
    path('schedule/', views.schedule, name='schedule'),
]
