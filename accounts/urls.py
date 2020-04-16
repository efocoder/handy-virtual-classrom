from django.urls import path
from . import views

urlpatterns =[
    path('register/', views.registerPage, name='registerPage'),
    path('login/', views.loginPage, name='loginPage'),
    path('logout/', views.logoutUser, name='logoutPage'),
    path('activate/<uidbase64>/<token>', views.activate, name='activate')

]