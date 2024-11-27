from django.views.generic import ListView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import UserIP


class UsersIpListView(LoginRequiredMixin, ListView):
    """
    Users Ip List View
    """

    login_url = reverse_lazy("login")
    template_name = "admin/admin_list_ip.html"
    model = UserIP
    context_object_name = "users_ip"
    queryset = UserIP.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["request"] = self.request
        return context


@csrf_exempt
def update_ip_block(request):
    if request.method == "POST":
        object_id = request.POST.get("id")
        is_checked = request.POST.get("is_checked") == "true"
        obj = get_object_or_404(UserIP, id=object_id)
        obj.is_blocked = is_checked
        obj.save()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False}, status=400)
