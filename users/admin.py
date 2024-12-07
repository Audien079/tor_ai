from django.contrib import admin
from users.models import User, UserIP, SearchLog


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    User data view in admin panel
    """

    list_display = ["id", "username", "email"]
    search_fields = ["username", "email"]


@admin.register(UserIP)
class UserIPAdmin(admin.ModelAdmin):
    """
    User IP Admin
    """
    list_display = ('ip_address', 'request_count', 'is_blocked')
    search_fields = ('ip_address',)


@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    """
    SearchLog Admin
    """
    list_display = ('keyword', 'user_ip')
    search_fields = ('keyword',)
