from django.contrib.auth import logout
from django.shortcuts import render, redirect


def authentication_login(request):
    return render(request, 'auth/login.html')


def authentication_logout(request):
    logout(request)

    return redirect('dashboard-login:logout')
