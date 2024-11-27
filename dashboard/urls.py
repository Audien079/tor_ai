from django.urls import path
from dashboard.views import HomeView, SearchView


urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='search'),
]
