from datetime import datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import JsonResponse
from django.views.generic import TemplateView
from users.utils import TrackUserIP
from users.models import SearchLog, UserIP


class HomeView(LoginRequiredMixin, TemplateView):
    """
    Clients page
    """
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SearchView(TemplateView):
    """
    Search view
    """
    template_name = "dashboard/search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        if query:
            is_blocked = TrackUserIP.track_ip(self.request, query)
            if is_blocked:
                context["blocked"] = True
                context['query'] = query

            else:
                sample_data = [
                    {"title": "Learn Django", "description": "Django is a high-level Python web framework.", "url": "https://example.com/"},
                    {"title": "Introduction to Python", "description": "Python is a versatile programming language.",
                     "url": "https://example.com/"},
                    {"title": "Learn JavaScript", "description": "JavaScript is essential for front-end web development.",
                     "url": "https://example.com/"},
                    {"title": "REST APIs", "description": "Learn how to build REST APIs using Django REST framework.",
                     "url": "https://example.com/"},
                ]

                if query:
                    filtered_data = [
                        item for item in sample_data
                        if query.lower() in item["title"].lower() or query.lower() in item["description"].lower()
                    ]
                else:
                    filtered_data = []

                context['data'] = filtered_data
                context['query'] = query
        return context


class ActivityView(TemplateView):
    """
    Activity page
    """
    template_name = "dashboard/activities.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users_ip"] = UserIP.objects.filter(is_blocked=False)
        # repeated_keywords = (
        #     Search.objects.values('keyword')
        #     .annotate(keyword_count=Count('keyword'))
        #     .filter(keyword_count__gt=1)
        # )
        return context


class BlcokedUsersView(TemplateView):
    """
    Blcoked Users page
    """
    template_name = "dashboard/blocked_users.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users_ip"] = UserIP.objects.filter(is_blocked=True)
        # repeated_keywords = (
        #     Search.objects.values('keyword')
        #     .annotate(keyword_count=Count('keyword'))
        #     .filter(keyword_count__gt=1)
        # )
        return context


class KeywordsView(TemplateView):
    """
    Keywords page
    """
    template_name = "dashboard/keywords.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["keywords"] = (
            SearchLog.objects.values('keyword')
            .annotate(keyword_count=Count('keyword'))
            .filter(keyword_count__gte=1)
        )
        return context
