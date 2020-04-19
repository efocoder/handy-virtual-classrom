from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='landing'),
    path('schedule/', views.schedule, name='schedule'),
    path('callback/', views.callback, name='callback'),
    path('connect/', views.connect, name='connect'),
    path('session/', views.session, name='session'),
]
