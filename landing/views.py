from django.shortcuts import render, redirect


def index(request):
    if not request.user.is_authenticated:
        return redirect('loginPage')

    return render(request, 'landing/index.html')
