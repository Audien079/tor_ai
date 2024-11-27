from django.urls import path
from admin_dashboard.views import UsersIpListView, update_ip_block


urlpatterns = [
    path('ips/', UsersIpListView.as_view(), name='user_ips'),
    path('update/ip/', update_ip_block, name='update_ip_block'),
]
