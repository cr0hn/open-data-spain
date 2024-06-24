from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'dashboard-api-keys'

urlpatterns = [
    path('api-keys/', login_required(views.api_keys_list), name='apikey-list'),
    path('api-keys/create/', login_required(views.api_keys_create), name='apikey-create'),
    path('api-keys/delete/<uuid:pk>/', login_required(views.api_keys_delete), name='apikey-delete'),
]
