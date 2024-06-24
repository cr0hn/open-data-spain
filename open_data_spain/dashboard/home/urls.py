from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'dashboard-home'

urlpatterns = [
    # Redirect to home
    path('', login_required(views.home), name='home'),
]
