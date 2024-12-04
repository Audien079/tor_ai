from django.urls import path
from dashboard.views import HomeView, SearchView, CustomersView, SettingsView


urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='search'),
    path('customers/', CustomersView.as_view(), name='customers'),
    path('settings/', SettingsView.as_view(), name='settings'),
]
