from django.urls import path

from . import views

app_name = 'user-api-v1_0'

urlpatterns = [
    path('me/', views.UserMe.as_view(), name='user-me'),
]
