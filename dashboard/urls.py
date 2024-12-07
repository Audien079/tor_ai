from django.urls import path
from dashboard.views import HomeView, SearchView, ActivityView, BlcokedUsersView, KeywordsView


urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='search'),
    path('activities/', ActivityView.as_view(), name='activities'),
    path('keywords/', KeywordsView.as_view(), name='keywords'),
    path('blocked/users/', BlcokedUsersView.as_view(), name='blocked_users'),
]
