from django.urls import path
from dashboard.views import HomeView


urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
]
