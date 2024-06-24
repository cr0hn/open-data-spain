from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'dashboard-login'

urlpatterns = [
    path('login/', views.authentication_login, name='login'),
    path('logout/', login_required(views.authentication_logout), name='logout'),
]
