from datetime import datetime, timedelta
from users.models import User
from django.http import JsonResponse
from django.views.generic import TemplateView
from users.utils import TrackUserIP


class HomeView(TemplateView):
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
        is_blocked = TrackUserIP.track_ip(self.request)
        if is_blocked:
            context["blocked"] = True

        else:
            # Sample data
            sample_data = [
                {"title": "Learn Django", "description": "Django is a high-level Python web framework.", "url": "https://example.com/"},
                {"title": "Introduction to Python", "description": "Python is a versatile programming language.",
                 "url": "https://example.com/"},
                {"title": "Learn JavaScript", "description": "JavaScript is essential for front-end web development.",
                 "url": "https://example.com/"},
                {"title": "REST APIs", "description": "Learn how to build REST APIs using Django REST framework.",
                 "url": "https://example.com/"},
            ]

            query = self.request.GET.get('q')

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


user_request_log = {}

def search_view(request):
    user_ip = get_client_ip(request)  # Get user IP address
    current_time = datetime.now()

    # Check if the user IP is already in the log
    if user_ip in user_request_log:
        request_times = user_request_log[user_ip]

        # Remove requests older than 5 minutes
        request_times = [t for t in request_times if t > current_time - timedelta(minutes=5)]

        # If there are recent requests within 10 seconds, block the user
        if len(request_times) > 0 and (current_time - request_times[-1]) < timedelta(seconds=10):
            return JsonResponse({"error": "Too many requests. You are temporarily blocked."}, status=429)

        # Add the current request time to the list
        request_times.append(current_time)
        user_request_log[user_ip] = request_times
    else:
        # Create a new entry for this user
        user_request_log[user_ip] = [current_time]

    # Handle the search query
    query = request.GET.get('q', '').strip()
    results = []  # Implement your search logic here

    # Example search results
    if query:
        results = [{"title": "Result 1", "description": "Description 1"},
                   {"title": "Result 2", "description": "Description 2"}]

    return JsonResponse({"results": results})
