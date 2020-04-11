from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from .forms import  CreateUserForm

def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Please confirm your email')
            # return redirect('loginPage')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)

