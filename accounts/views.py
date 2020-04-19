import os

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage, send_mail


from .forms import CreateUserForm
from .models import MyUser
from .utils import generate_token



def registerPage(request):
    if request.user.is_authenticated:
        messages.info(request, 'Already logged in')
        return redirect('landing')

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            activate_msg(request, user)

            messages.success(request, 'Please confirm your email')
            return redirect('loginPage')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        messages.info(request, 'Already logged in')
        return redirect('landing')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('landing')
        else:
            messages.error(request, 'Invalid credentials ')

    return render(request, 'accounts/login.html')


def logoutUser(request):
    print(request.user)
    logout(request)
    print(request.user)
    return redirect('home')


def activate(request, uidbase64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidbase64))
        user = MyUser.objects.get(pk=uid)
    except Exception as e:
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'account activated successfully')

        return redirect('loginPage')

    return render(request, 'accounts/activate_failed.html', status=401)


def activate_msg(request, user):
    print("###########################")
    print('This is the user', user)
    print('This is the request', request)
    print("###########################")
    current_site = get_current_site(request)
    email_subject = "Activate your Account"
    message = render_to_string('accounts/activate.html',
                               {
                                   'user': user,
                                   'domain': current_site.domain,
                                   'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                   'token': generate_token.make_token(user)
                               }
                               )
    # email = EmailMessage(
    #     email_subject,
    #     message,
    #     'HVC',
    #     [user.email],
    # )
    # email.send()

    send_mail(
        email_subject,
        message,
        'HVC',
        [user.email],
        fail_silently=False,
    )
