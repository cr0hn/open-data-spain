from django.urls import path, include

urlpatterns = [
    # Redirect to home
    path('dashboard/', include('dashboard.home.urls')),
    path('dashboard/', include('dashboard.billing.urls')),
    path('dashboard/', include('dashboard.api_keys.urls')),
    path('authentication/', include('dashboard.login.urls')),
]
