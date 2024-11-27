from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('super-admin/', admin.site.urls),
    path('admin/', include('admin_dashboard.urls')),
    path('', include('users.urls')),
    path('', include('dashboard.urls')),
]
